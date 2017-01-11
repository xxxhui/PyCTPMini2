# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 13:50 2016
@author: YuWangying
"""

import sys
import time
import os
import threading
import chardet
from PyQt4 import QtCore
from PyQt4.QtGui import QApplication, QCompleter, QLineEdit, QStringListModel
import pandas as pd
from pandas import Series, DataFrame
from pymongo import MongoClient
from DBManager import DBManger
from PyCTP_Trade import PyCTP_Trader_API
from PyCTP_Market import PyCTP_Market_API
import Utils
from Trader import Trader
from User import User
from Strategy import Strategy
from MarketManager import MarketManager
from QAccountWidget import QAccountWidget
from QNewStrategy import QNewStrategy
from QMessageBox import QMessageBox
from collections import namedtuple  # Socket所需package
import socket
import struct


class CTPManager(QtCore.QObject):
    signal_UI_remove_strategy = QtCore.pyqtSignal(object)  # 定义信号：删除界面策略
    signal_insert_strategy = QtCore.pyqtSignal(object)  # 定义信号：添加界面策略
    signal_hide_QNewStrategy = QtCore.pyqtSignal()  # 定义信号：隐藏创建策略的小弹窗
    signal_UI_update_pushButton_start_strategy = QtCore.pyqtSignal(dict)  # 定义信号：更新界面“开始策略”按钮
    signal_create_QAccountWidget = QtCore.pyqtSignal()  # 定义信号：创建QAccountWidget窗口
    signal_update_pushButton_start_strategy = QtCore.pyqtSignal()  # 定义信号：内核设置交易员交易开关 -> 更新窗口“开始策略”按钮状态
    signal_remove_strategy = QtCore.pyqtSignal(object)  # 定义信号：内核删除策略 -> 窗口删除策略
    signal_label_login_error_text = QtCore.pyqtSignal(str)  # 定义信号：设置登录界面的消息框文本
    signal_show_QMessageBox = QtCore.pyqtSignal(list)  # 定义信号：CTPManager初始化过程中(子线程)需要弹窗 -> ClientMain(主线程)中槽函数调用弹窗

    def __init__(self, parent=None):
        super(CTPManager, self).__init__(parent)  # 显示调用父类初始化方法，使用其信号槽机制
        # self.__DBManager = DBManger()  # 创建数据库连接
        self.__MarketManager = None  # 行情管理实例，MarketManager
        self.__trader = None  # 交易员实例
        self.__list_user = list()  # 存放user对象的list
        # 字典结构 {'063802': {'connect_trade_front': 0, 'QryTrade': 0, 'QryTradingAccount': 0, 'QryOrder': 0, 'QryInvestorPosition': 0, 'login_trade_account': 0}}
        self.__dict_user = dict()
        self.__list_strategy = list()  # 交易策略实例list
        self.__list_instrument_info = list()  # 期货合约信息
        self.__got_list_instrument_info = False  # 获得了期货合约信息
        self.__on_off = 0  # 交易员的交易开关，初始值为关
        self.__only_close = 0  # 交易员的只平，初始值为关
        self.__init_finished = False  # 内核初始化状态，False未完成、True完成
        self.__init_UI_finished = False  # 界面初始化状态，False未完成、True完成
        self.__list_QAccountWidget = list()  # 存放窗口对象的list
        self.__thread_init = threading.Thread(target=self.start_init)  # 创建初始化内核方法线程
        self.signal_create_QAccountWidget.connect(self.create_QAccountWidget)  # 定义信号：调用本类的槽函数（因信号是在子进程里发出）
        self.__list_user_info = list()  # 从服务端收到的user信息list初始值
        self.__list_user_will_create = list()  # 将要创建成功的期货账户信息列表
        self.__list_strategy_info = list()  # 从服务端收到的策略信息list初始值
        self.__list_strategy_will_create = list()  # 创建成功期货账户的策略列表初始值

    @QtCore.pyqtSlot()
    def init(self):
        self.__thread_init.start()

    # 初始化（独立线程）
    def start_init(self):
        thread = threading.current_thread()
        print(">>> CTPManager.start_init() thread.getName()=", thread.getName())
        
        """创建行情实例"""
        self.signal_label_login_error_text.emit("登录行情")
        if len(self.__socket_manager.get_list_market_info()) > 0:
            result_create_md = self.create_md(self.__socket_manager.get_list_market_info()[0])
            if result_create_md is False:
                # QMessageBox().showMessage("警告", "创建行情失败")
                self.signal_show_QMessageBox.emit(["警告", "创建行情失败"])
                return  # 结束程序：创建行情失败
        else:
            # QMessageBox().showMessage("警告", "没有行情地址")
            self.signal_show_QMessageBox.emit(["警告", "没有行情地址"])

        """创建期货账户"""
        self.signal_label_login_error_text.emit("登录期货账户")
        # 如果期货账户数量为0，向界面弹窗
        users = len(self.__socket_manager.get_list_user_info())  # 将要创建期货账户数量
        if users == 0:
            # QMessageBox().showMessage("警告", "将要创建期货账户数量为0")
            self.signal_show_QMessageBox.emit(["警告", "将要创建期货账户数量为0"])
        dict_create_user_failed = {}  # 创建失败的期货账户列表
        # print(">>> CTPManager.start_init() 将要创建期货账户数量users=", users)
        for i in self.__socket_manager.get_list_user_info():
            self.create_user(i)  # 创建期货账户
        for i in self.__dict_user:
            # print(">>> CTPManager.start_init() len(self.__dict_user[i])=", len(self.__dict_user[i]))
            for j in self.__dict_user[i]:
                # print(">>> CTPManager.start_init() user_id=", i, j, "=", self.__dict_user[i][j])
                if self.__dict_user[i][j] != 0:
                    users -= 1  # 成功创建期货账户数量减一
                    dict_create_user_failed[i] = {j: self.__dict_user[i][j]}  # 统计创建失败的期货账户
                    # print(">>> CTPManager.start_init() dict_create_user_failed[i]=", dict_create_user_failed[i])
        # print(">>> CTPManager.start_init() 成功创建期货账户数量users=", users)
        # print(">>> CTPManager.start_init() len(self.__list_user)=", len(self.__list_user))
        # 存在创建失败的期货账户，但成功创建的期货账户数量大于0，向界面弹窗
        if users < len(self.__socket_manager.get_list_user_info()) and users > 0:
            str_print = "以下期货账户创建失败\n"
            for i in dict_create_user_failed:
                for j in dict_create_user_failed[i]:
                    if dict_create_user_failed[i][j] != 0:
                        str_print = str_print + i + ":" + j + "原因" + str(dict_create_user_failed[i][j]) + "\n"
            # QMessageBox().showMessage("警告", str_print)
            self.signal_show_QMessageBox.emit(["警告", str_print])
        # 成功创建期货账户的数量为0，向界面弹窗
        elif users == 0:
            # QMessageBox().showMessage("警告", "成功创建期货账户的数量为0")
            self.signal_show_QMessageBox.emit(["警告", "成功创建期货账户的数量为0"])
            return  # 结束程序：创建期货账户失败

        """创建策略"""
        self.signal_label_login_error_text.emit("创建策略")
        self.__list_strategy_info = self.__socket_manager.get_list_strategy_info()  # 获取所有策略信息列表
        # print(">>> CTPManager.start_init() self.__list_strategy_info=", self.__list_strategy_info)
        if len(self.__list_strategy_info) > 0:
            # 过滤出创建成功的期货账户的策略
            for i_strategy in self.__list_strategy_info:
                for i_user in self.__list_user:
                    # print(">>> CTPManager.start_init() i_strategy['user_id'] == i_user.get_user_id().decode()", i_strategy['user_id'], i_user.get_user_id().decode())
                    if i_strategy['user_id'] == i_user.get_user_id().decode():
                        self.__list_strategy_will_create.append(i_strategy)
                        # print(">>> CTPManager.start_init() self.__list_strategy_will_create=", len(self.__list_strategy_will_create), self.__list_strategy_will_create)
                        break
        # print(">>> CTPManager.start_init() self.__list_strategy_will_create=", self.__list_strategy_will_create)

        # 创建策略
        if len(self.__list_strategy_will_create) > 0:
            for i in self.__list_strategy_will_create:
                self.create_strategy(i)  # 创建策略
        elif len(self.__list_strategy_will_create) == 0:
            self.__init_finished = True  # CTPManager初始化完成，跳转到界面初始化或显示

        if self.__init_finished:  # 如果CTPManager初始化完成，跳转到界面初始化或显示
            self.signal_create_QAccountWidget.emit()  # 创建窗口界面
            # self.create_QAccountWidget()  # 创建窗口界面

    # 创建MD
    def create_md(self, dict_arguments):
        # dict_arguments = {'front_address': 'tcp://180.168.146.187:10010', 'broker_id': '9999'}
        # 创建行情管理实例MarketManager
        self.__MarketManager = MarketManager(dict_arguments['frontaddress'],
                                             dict_arguments['brokerid'],
                                             dict_arguments['userid'],
                                             dict_arguments['password']
                                             )
        self.__MarketManager.get_market().set_strategy(self.__list_strategy)  # 将策略列表设置为Market_API类的属性
        if self.__MarketManager.get_result_market_connect() == 0 and self.__MarketManager.get_result_market_login() == 0:
            print("CTPManager.create_md() 创建行情成功，交易日=", self.__MarketManager.get_market().GetTradingDay())  # 行情API中获取到的交易日
            return True
        else:
            print("CTPManager.create_md() 创建行情失败")
            return False

    # 创建trader
    def create_trader(self, dict_arguments):
        self.__trader = Trader(dict_arguments)
        self.__trader_id = self.__trader.get_trader_id()

    # 创建user(期货账户)
    def create_user(self, dict_arguments):
        # 不允许重复创建期货账户实例
        if len(self.__list_user) > 0:
            for i in self.__list_user:
                if i.get_user_id() == dict_arguments['userid']:
                    print("MultiUserTraderSys.create_user()已经存在user_id为", dict_arguments['userid'], "的实例，不允许重复创建")
                    return
        obj_user = User(dict_arguments, ctp_manager=self)
        # 将创建成功的期货账户对象存放到self.__list_user
        for i in self.__dict_user:
            if i == obj_user.get_user_id().decode():
                if self.__dict_user[i]['connect_trade_front'] == 0 \
                        and self.__dict_user[i]['login_trade_account'] == 0 \
                        and self.__dict_user[i]['QryTradingAccount'] == 0 \
                        and self.__dict_user[i]['QryInvestorPosition'] == 0 \
                        and self.__dict_user[i]['QryTrade'] == 0 \
                        and self.__dict_user[i]['QryOrder'] == 0 :
                    obj_user.set_CTPManager(self)  # 将CTPManager类设置为user的属性
                    time.sleep(1.0)
                    obj_user.qry_instrument_info()  # 查询合约信息
                    self.__list_user.append(obj_user)  # user类实例添加到列表存放
                    print("CTPManager.create_user() 创建期货账户成功，user_id=", dict_arguments['userid'])
                else:
                    print("CTPManager.create_user() 创建期货账户失败，user_id=", dict_arguments['userid'])

        # if self.__dict_user[dict_arguments['userid']] == 1:  # 判断是否成功创建期货账户
        #     # obj_user.set_DBManager(self.__DBManager)  # 将数据库管理类设置为user的属性
        #     obj_user.set_CTPManager(self)  # 将CTPManager类设置为user的属性
        #     obj_user.qry_instrument_info()  # 查询合约信息
        #     self.__list_user.append(obj_user)  # user类实例添加到列表存放
        #     print("CTPManager.create_user() 创建期货账户成功，user_id=", dict_arguments['userid'])
        # elif self.__dict_user[dict_arguments['userid']] == 0:
        #     print("CTPManager.create_user() 创建期货账户失败，user_id=", dict_arguments['userid'])

    # 将strategy对象添加到user里
    def add_strategy_to_user(self, obj_strategy):
        for i in self.__list_user:
            if i.get_user_id() == obj_strategy.get_user_id():
                i.add_strategy()

    # 创建strategy
    def create_strategy(self, dict_arguments):
        # 不允许重复创建策略实例
        if len(self.__list_strategy) > 0:
            for i in self.__list_strategy:
                if i.get_strategy_id() == dict_arguments['strategy_id'] and i.get_user_id() == dict_arguments['user_id']:
                    print("CTPManager.create_strategy() 不能重复创建，已经存在user_id=", dict_arguments['user_id'], "strategy_id=", dict_arguments['strategy_id'])
                    return False

        # 遍历user对象列表，找到将要创建策略所属的user对象
        for i_user in self.__list_user:
            if i_user.get_user_id().decode() == dict_arguments['user_id']:  # 找到策略所属的user实例
                # 创建策略
                obj_strategy = Strategy(dict_arguments, i_user)  # 创建策略实例，user实例和数据库连接实例设置为strategy的属性
                # obj_strategy.set_DBManager(self.__DBManager)
                i_user.add_strategy(obj_strategy)               # 将策略实例添加到user的策略列表
                self.__list_strategy.append(obj_strategy)  # 将策略实例添加到CTP_Manager的策略列表
                print("CTPManager.create_strategy() 创建策略，user_id=", dict_arguments['user_id'], "strategy_id=", dict_arguments['strategy_id'])
                # 为策略订阅行情
                list_instrument_id = list()
                for i in dict_arguments['list_instrument_id']:
                    list_instrument_id.append(i.encode())  # 将合约代码转码为二进制字符串
                self.__MarketManager.sub_market(list_instrument_id, dict_arguments['user_id'], dict_arguments['strategy_id'])

        # 判断内核是否初始化完成（所有策略是否初始化完成）
        if self.__init_finished:  # 内核初始化完成、程序运行中新添加策略，在界面策略列表框内添加一行
            print(">>> CTPManager.create_strategy() 程序运行中添加策略", dict_arguments['strategy_id'])
            self.signal_insert_strategy.emit(obj_strategy)  # 内核向界面插入策略
            self.signal_hide_QNewStrategy.emit()  # 隐藏创建策略的小弹窗
        elif self.__init_finished is False:  # 内核初始化未完成
            # 最后一个策略初始化完成，将内核初始化完成标志设置为True
            if self.__list_strategy_info[-1]['user_id'] == dict_arguments['user_id'] and \
                            self.__list_strategy_info[-1]['strategy_id'] == dict_arguments['strategy_id']:
                self.__init_finished = True  # CTPManager初始化完成

    # 删除strategy
    def delete_strategy(self, dict_arguments):
        print("CTPManager.delete_strategy() 删除策略对象", dict_arguments)

        # 将obj_strategy从CTPManager的self.__list_strategy中删除
        for i_strategy in self.__list_strategy:
            if i_strategy.get_user_id() == dict_arguments['user_id'] and i_strategy.get_strategy_id() == dict_arguments['strategy_id']:
                # 退订该策略的行情
                self.__MarketManager.un_sub_market(i_strategy.get_list_instrument_id(),
                                                   dict_arguments['user_id'],
                                                   dict_arguments['strategy_id'])
                self.__list_strategy.remove(i_strategy)
                break

        # 将obj_strategy从user中的list_strategy中删除
        for i_user in self.__list_user:
            if i_user.get_user_id().decode() == dict_arguments['user_id']:
                for i_strategy in i_user.get_list_strategy():
                    if i_strategy.get_strategy_id() == dict_arguments['strategy_id']:
                        i_user.get_list_strategy().remove(i_strategy)
                        self.signal_remove_strategy.emit(i_strategy)  # 发送信号，从界面中删除策略
                        break
                break
        for i_strategy in self.__list_strategy:
            print("user_id=", i_strategy.get_user_id(), "strategy_id=", i_strategy.get_strategy_id())

        # 内核删除策略成功，通知界面删除策略
        # self.signal_remove_row_table_widget.emit()  # 在界面策略列表中删除策略

    # 修改策略,(SocketManager收到服务端修改策略参数类回报 -> CTPManager修改策略)
    @QtCore.pyqtSlot(dict)
    def slot_update_strategy(self, dict_arguments):
        # 对收到的消息做筛选，教给对应的策略
        pass

    # 初始化账户窗口
    def create_QAccountWidget(self):
        QApplication.processEvents()
        print(">>> CTPManager.create_QAccountWidget() 创建“新建策略”窗口=", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # print(">>> CTPManager.create_QAccountWidget() CTPManager内核初始化完成，开始创建窗口")

        """创建“新建策略”窗口"""
        self.create_QNewStrategy()

        print(">>> CTPManager.create_QAccountWidget() 开始创建总账户窗口=",
              time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        """创建总账户窗口"""
        if True:
            QAccountWidget_total = QAccountWidget(str_widget_name='总账户', 
                                                  list_user=self.get_list_user(),
                                                  ClientMain=self.__client_main,
                                                  CTPManager=self,
                                                  SocketManager=self.__socket_manager)
            # 总账户窗口设置为所有user的属性
            for i_user in self.get_list_user():
                QApplication.processEvents()
                i_user.set_QAccountWidget_total(QAccountWidget_total)
            # 总账户窗口设置为所有strategy的属性
            for i_strategy in self.get_list_strategy():
                QApplication.processEvents()
                i_strategy.set_QAccountWidget_total(QAccountWidget_total)
                # 信号槽连接：策略对象修改策略 -> 窗口对象更新策略显示（Strategy.signal_update_strategy -> QAccountWidget.slot_update_strategy() ）
                # i_strategy.signal_update_strategy.connect(QAccountWidget_total.slot_update_strategy)
                # 信号槽连接：策略对象价差值变化 -> 窗口对象更新价差（Strategy.signal_UI_update_spread_total -> QAccountWidget.slot_update_spread()）
                # i_strategy.signal_UI_update_spread_total.connect(QAccountWidget_total.slot_update_spread)
            # 所有策略列表设置为窗口属性
            QAccountWidget_total.set_list_strategy(self.__list_strategy)
            self.__list_QAccountWidget.append(QAccountWidget_total)  # 将窗口对象存放到list集合里
            # self.signal_pushButton_set_position_setEnabled.connect(QAccountWidget_total.on_pushButton_set_position_active)
            # QAccountWidget_total.set_signal_pushButton_set_position_setEnabled_connected(True)  # 信号槽绑定标志设置为True

            # 绑定信号槽：设置交易员交易开关 -> 更新总账户窗口“开始策略”按钮状态
            self.signal_update_pushButton_start_strategy.connect(QAccountWidget_total.slot_update_pushButton_start_strategy)

        print(">>> CTPManager.create_QAccountWidget() 创建单账户窗口=", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        """创建单账户窗口"""
        for i_user in self.get_list_user():
            QApplication.processEvents()
            QAccountWidget_single = QAccountWidget(str_widget_name=i_user.get_user_id().decode(),
                                                   obj_user=i_user,
                                                   ClientMain=self.__client_main,
                                                   CTPManager=self,
                                                   SocketManager=self.__socket_manager)
            # 单账户窗口设置为对应的user的属性
            i_user.set_QAccountWidget_signal(QAccountWidget_single)

            # 单账户窗口设置为对应期货账户的所有策略的属性
            for i_strategy in i_user.get_list_strategy():
                QApplication.processEvents()
                i_strategy.set_QAccountWidget_signal(QAccountWidget_single)
                # 信号槽连接：策略对象修改策略 -> 窗口对象更新策略显示（Strategy.signal_update_strategy -> QAccountWidget.slot_update_strategy() ）
                # i_strategy.signal_update_strategy.connect(QAccountWidget_single.slot_update_strategy)
                # 信号槽连接：策略对象价差值变化 -> 窗口对象更新价差（Strategy.signal_UI_update_spread_signal -> QAccountWidget.slot_update_spread()）
                # i_strategy.signal_UI_update_spread_signal.connect(QAccountWidget_single.slot_update_spread)
            # 单期货账户的所有策略列表设置为窗口属性
            QAccountWidget_single.set_list_strategy(i_user.get_list_strategy())
            self.__list_QAccountWidget.append(QAccountWidget_single)  # 将窗口对象存放到list集合里
            # self.signal_pushButton_set_position_setEnabled.connect(QAccountWidget_single.on_pushButton_set_position_active)
            # QAccountWidget_single.set_signal_pushButton_set_position_setEnabled_connected(True)  # 信号槽绑定标志设置为True

            # 绑定信号槽：设置期货账户交易开关 -> 更新单期货账户窗口“开始策略”按钮状态
            i_user.signal_update_pushButton_start_strategy.connect(QAccountWidget_single.slot_update_pushButton_start_strategy)

        self.__client_main.set_list_QAccountWidget(self.__list_QAccountWidget)  # 窗口对象列表设置为ClientMain的属性

        print(">>> CTPManager.create_QAccountWidget() 窗口添加到tab_accounts=", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        """窗口添加到tab_accounts"""
        for i_widget in self.__list_QAccountWidget:
            QApplication.processEvents()
            self.__q_ctp.tab_accounts.addTab(i_widget, i_widget.get_widget_name())  # 将账户窗口添加到tab_accounts窗体里
            """信号槽连接"""
            # 下面注释代码位置转移到QAccountWidget.slot_insert_strategy()里，向窗口插入策略的时候动态绑定策略与窗口之间的信号槽关系
            # 信号槽：CTPManager创建策略 -> QAccountWidget插入策略（CTPManager.signal_insert_strategy -> QAccountWidget.slot_insert_strategy()）
            self.signal_insert_strategy.connect(i_widget.slot_insert_strategy)
            # 窗口修改策略 -> SocketManager发送修改指令（QAccountWidget.signal_send_msg -> SocketManager.slot_send_msg() ）
            i_widget.signal_send_msg.connect(self.__socket_manager.slot_send_msg)
            # 绑定信号槽：收到服务端的查询策略信息 -> groupBox界面状态还原（激活查询按钮、恢复“设置持仓”按钮）
            self.__socket_manager.signal_restore_groupBox.connect(i_widget.slot_restore_groupBox_pushButton)
            # 绑定信号槽：内核删除策略 -> 界面删除策略
            self.signal_remove_strategy.connect(i_widget.slot_remove_strategy)

        print(">>> CTPManager.create_QAccountWidget() 向界面插入策略=", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        """向界面插入策略"""
        for i_strategy in self.get_list_strategy():
            QApplication.processEvents()
            self.signal_insert_strategy.emit(i_strategy)  # 向界面插入策略

        """初始化开始策略按钮状态"""
        self.signal_update_pushButton_start_strategy.emit()  # 向总账户窗口发送信号
        for i_user in self.__list_user:
            i_user.signal_update_pushButton_start_strategy.emit()  # 向单账户窗口发送信号

        self.__init_UI_finished = True  # 界面初始化完成标志位
        self.__client_main.set_init_UI_finished(True)  # 界面初始化完成标志位设置为ClientMain的属性

        print(">>> CTPManager.create_QAccountWidget() 显示主窗口=", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.__q_ctp.show()  # 显示主窗口
        print(">>> CTPManager.create_QAccountWidget() 隐藏登录窗口=", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.__q_login_form.hide()  # 隐藏登录窗口

        print(">>> CTPManager.create_QAccountWidget() 结束时间=", time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print(">>> ClientMain.create_QAccountWidget() 界面初始化完成")

    # 创建“新建策略窗口”
    def create_QNewStrategy(self):
        self.__q_new_strategy = QNewStrategy()
        completer = QCompleter()
        if self.get_got_list_instrument_info():
            model = QStringListModel()
            model.setStringList(self.get_list_instrument_id())
            completer.setModel(model)
        else:
            print(">>> CTPManager.create_QNewStrategy() 查询合约信息失败")
        self.__q_new_strategy.lineEdit_a_instrument.setCompleter(completer)
        self.__q_new_strategy.lineEdit_b_instrument.setCompleter(completer)
        self.__q_new_strategy.set_ClientMain(self.__client_main)  # CTPManager设置为新建策略窗口属性
        self.__q_new_strategy.set_CTPManager(self)  # CTPManager设置为新建策略窗口属性
        self.__q_new_strategy.set_SocketManager(self.__socket_manager)  # SocketManager设置为新建策略窗口属性
        self.__q_new_strategy.set_trader_id(self.__trader_id)  # 设置trade_id属性
        self.set_QNewStrategy(self.__q_new_strategy)  # 新建策略窗口设置为CTPManager属性
        self.__client_main.set_QNewStrategy(self.__q_new_strategy)  # 新建策略窗口设置为ClientMain属性
        self.signal_hide_QNewStrategy.connect(self.get_QNewStrategy().hide)  # 绑定信号槽，新创建策略成功后隐藏“新建策略弹窗”
        # 绑定信号槽：新建策略窗新建策略指令 -> SocketManager.slot_send_msg
        self.__q_new_strategy.signal_send_msg.connect(self.__socket_manager.slot_send_msg)

    # 创建数据库连接实例
    def create_DBManager(self):
        self.__DBManager = DBManger()

    # 获取数据库连接实例
    def get_mdb(self):
        return self.__DBManager

    # 获取行情实例
    def get_md(self):
        return self.__MarketManager

    # 获取trader对象的list
    def get_trader(self):
        return self.__trader

    # 获取user对象的list
    def get_list_user(self):
        return self.__list_user

    # 获取strategy对象的list
    def get_list_strategy(self):
        return self.__list_strategy

    # 获取user对象创建状态的dict
    def get_dict_user(self):
        return self.__dict_user

    # 设置CTPManager内核初始化完成
    def set_init_finished(self, bool_input):
        print(">>> CTPManager.set_init_finished() CTPManager内核初始化完成")
        self.__init_finished = bool_input

    # 获取CTPManager内核初始化状态
    def get_init_finished(self):
        return self.__init_finished

    # 设置界面初始化状态
    def set_init_UI_finished(self, bool_input):
        self.__init_UI_finished = bool_input

    def get_init_UI_finished(self):
        return self.__init_UI_finished

    # 从user对象列表里找到指定user_id的user对象
    def find_user(self, user_id):
        for i in self.__list_user:
            if i.get_user_id() == user_id:
                return i

    def set_ClientMain(self, obj_ClientMain):
        self.__client_main = obj_ClientMain

    def get_ClientMain(self):
        return self.__client_main

    def set_SocketManager(self, obj_SocketManager):
        self.__socket_manager = obj_SocketManager

    def get_SocketManager(self):
        return self.__socket_manager

    def set_QLoginForm(self, obj_QLoginForm):
        self.__q_login_form = obj_QLoginForm

    def get_QLoginForm(self):
        return self.__q_login_form

    def set_QCTP(self, obj_QCTP):
        self.__q_ctp = obj_QCTP

    def get_QCTP(self):
        return self.__q_ctp

    def set_QNewStrategy(self, obj_QNewStrategy):
        self.__q_new_strategy = obj_QNewStrategy

    def get_QNewStrategy(self):
        return self.__q_new_strategy

    def set_list_market_info(self, list_input):
        self.__list_market_info = list_input

    def get_list_market_info(self):
        return self.__list_market_info
        
    def set_list_user_info(self, list_input):
        self.__list_user_info = list_input

    def get_list_user_info(self):
        return self.__list_user_info

    # 所有策略的昨仓保存到一个list，从服务端查询获得
    def set_YesterdayPosition(self, listYesterdayPosition):
        self.__listYesterdayPosition = listYesterdayPosition

    def get_YesterdayPosition(self):
        return self.__listYesterdayPosition

    # 新增trader_id下面的某个期货账户
    def add_user(self, trader_id, broker_id, front_address, user_id, password):
        print('add_user(): trader_id=', trader_id, 'broker_id=', broker_id, 'user_id=', user_id)
        add_user_arguments = {'trader_id': trader_id,
                              'broker_id': broker_id,
                              'UserID': user_id,
                              'Password': password,
                              'front_address': front_address}
        # 新增期货账户，创建TradeApi实例
        return User(add_user_arguments)
    
    # 删除trader_id下面的某个期货账户
    # 参数说明： user=class User实例名称
    def del_user(self, user, trader_id, broker_id, front_address, user_id):
        print('del_user(): trader_id=', trader_id, 'broker_id=', broker_id, 'user_id=', user_id)
        del_user_arguments = {'trader_id': trader_id,
                              'broker_id': broker_id,
                              'UserID': user_id,
                              'front_address': front_address}
        # 删除期货账户，释放TradeApi实例
        user.UnConnect()
        # 操作MongoDB，删除Operator下面的user_id（期货账户）
    
    # 交易员登录验证
    def trader_login(self, trader_id, password):
        return self.__DBManager.check_trader(trader_id, password)

    # 设置交易员id
    def set_trader_id(self, str_TraderID):
        self.__trader_id = str_TraderID

    # 获得交易员id
    def get_trader_id(self):
        return self.__trader_id

    def set_trader_name(self, str_trader_name):
        self.__trader_name = str_trader_name

    def get_trader_name(self):
        return self.__trader_name

    # 设置客户端的交易开关，0关、1开
    def set_on_off(self, int_on_off):
        # print(">>> CTPManager.set_on_off()", int_on_off)
        self.__on_off = int_on_off
        self.signal_update_pushButton_start_strategy.emit()  # 触发信号：内核设置交易员交易开关 -> 更新窗口“开始策略”按钮状态

    # 获取客户端的交易开关，0关、1开
    def get_on_off(self):
        return self.__on_off

    # 设置交易开关，0关、1开
    def set_only_close(self, int_only_close):
        self.__only_close = int_only_close

    # 获取交易开关，0关、1开
    def get_only_close(self):
        return self.__only_close

    # 设置“已经获取到合约信息的状态”
    def set_got_list_instrument_info(self, bool_status):
        self.__got_list_instrument_info = bool_status

    # 获取“已经获取到合约信息的状态”
    def get_got_list_instrument_info(self):
        return self.__got_list_instrument_info

    # 设置合约信息
    def set_instrument_info(self, input_list):
        self.__list_instrument_info = input_list
        self.__list_instrument_id = list()
        for i in self.__list_instrument_info:
            self.__list_instrument_id.append(i['InstrumentID'])

    # 获取合约信息
    def get_instrument_info(self):
        return self.__list_instrument_info

    # 获取期货合约代码列表
    def get_list_instrument_id(self):
        return self.__list_instrument_id



