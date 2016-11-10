# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 08:46:13 2016

@author: YuWanying
"""

import time
import datetime
from pymongo import MongoClient
from PyCTP_Trade import PyCTP_Trader_API
import Utils
from pandas import DataFrame, Series


class User:
    # 初始化参数BrokerID\UserID\Password\frontaddress，参数格式为二进制字符串
    def __init__(self, dict_arguments):
        print('User.__init__()', dict_arguments)
        self.__trader_id = dict_arguments['traderid'].encode()
        self.__user_id = dict_arguments['userid'].encode()
        self.__BrokerID = dict_arguments['brokerid'].encode()
        self.__Password = dict_arguments['password'].encode()
        self.__FrontAddress = dict_arguments['frontaddress'].encode()

        self.__list_OnRtnOrder = []  # 保存单账户所有的OnRtnOrder回调数据
        self.__list_OnRtnTrade = []  # 保存单账户所有的OnRtnTrade回调数据
        self.__list_order_ing = []  # 以OrderRef为单个交易单元，还未执行完成的订单列表，临时存放较少的数据
        self.__list_SendOrder = []  # 保存单账户所有调用OrderInsert的记录
        self.__list_strategy = []  # 期货账户下面的所有交易策略实例列表
        # self.__list_InstrumentId = []  # 合约列表，记录撤单次数，在创建策略的时候添加合约，
        self.__dict_instrument_action_counter = dict()  # 记录合约撤单次数的字典,撤单操作时添加次数，交易日换日时初始化值
        self.__order_ref_part2 = 0  # 所有策略共用报单引用编号

        # 联机登录：创建user时清空本地数据库中的集合：col_strategy、col_position、col_position_detail、col_trade、col_order，
        # 脱机登录：创建user时清空本地数据库中的集合：col_strategy、col_position、col_position_detail、col_trade、col_order，
        # 其中trade和order记录只清空当天的
        self.__mongo_client = MongoClient('localhost', 27017)  # 创建数据库连接实例
        col_strategy = self.__user_id.decode() + 'strategy'  # 策略集合名
        col_position = self.__user_id.decode() + 'position'  # 持仓汇总集合名
        col_position_detail = self.__user_id.decode() + 'position_detail'  # 持仓明细集合名
        col_trade = self.__user_id.decode() + 'trade'  # trade回调记录集合名
        col_order = self.__user_id.decode() + 'order'  # order回调记录集合名
        for i in [col_strategy, col_position, col_position_detail]:  # 初始化user时清空集合
            try:
                self.__mongo_client.CTP.drop_collection(i)
            except:
                print("User.__init__() 删除数据库集合失败，集合名=", i)
        for i in [col_trade, col_order]:  # 初始化user时清空当天Trade、Order集合
            try:
                self.__mongo_client.CTP.get_collection(i).delete_many({'TradingDay': self.__TradingDay})
            except:
                print("User.__init__() 删除当天的trade或order记录失败")

        # 为每个user创建独立的流文件夹
        s_path = b'conn/td/' + self.__user_id + b'/'
        Utils.make_dirs(s_path)  # 创建流文件路劲
        self.__trade = PyCTP_Trader_API.CreateFtdcTraderApi(s_path)
        self.__trade.set_user(self)  # 将该类设置为trade的属性
        print('===========================')
        print(self.__user_id, '连接交易前置', Utils.code_transform(self.__trade.Connect(self.__FrontAddress)))
        print(self.__user_id, '登陆交易账号', Utils.code_transform(self.__trade.Login(self.__BrokerID, self.__user_id, self.__Password)))
        print(self.__user_id, '交易日', Utils.code_transform(self.__trade.GetTradingDay()))
        time.sleep(1.0)
        print(self.__user_id, '投资者代码', Utils.code_transform(self.__trade.setInvestorID(self.__user_id)))
        self.__front_id = self.__trade.get_front_id()  # 获取前置编号
        self.__session_id = self.__trade.get_session_id()  # 获取会话编号
        self.__TradingDay = self.__trade.GetTradingDay().decode()  # 获取交易日

        self.__on_off = 1  # 策略交易开关，0关、1开

        self.__init_finished = False  # 初始化完成

        self.__dfQryTrade = DataFrame()  # 查询交易、委托记录
        self.__dfQryOrder = DataFrame()
        self.QryTrade()  # 获取user的Trade记录
        time.sleep(1.0)
        self.QryOrder()  # 获取user的Order记录
        time.sleep(1.0)

    # 设置合约信息
    def set_InstrumentInfo(self, list_InstrumentInfo):
        self.__instrument_info = list_InstrumentInfo

    # 查询合约信息
    def qry_instrument_info(self):
        if self.__CTPManager.get_got_list_instrument_info() is False:
            self.__instrument_info = Utils.code_transform(self.qry_instrument())  # 查询合约，所有交易所的所有合约
            self.__CTPManager.set_list_instrument_info(self.__instrument_info)  # 将查询到的合约信息传递给CTPManager
            if len(self.__instrument_info) > 0:
                self.__CTPManager.set_got_list_instrument_info(True)  # 将获取合约信息的状态设置为真，获取成功

    # time.sleep(1.0)
    # print("User.__init__.self.__instrument_info=", self.__instrument_info)

    # 将CTPManager类设置为user的属性
    def set_CTPManager(self, obj_CTPManager):
        self.__CTPManager = obj_CTPManager

    # 获取CTPManager属性
    def get_CTPManager(self):
        return self.__CTPManager

    # 设置数据库管理类DBManager为该类对象
    def set_DBManager(self, obj_DBManager):
        self.__DBManager = obj_DBManager

    # 获得数据库
    def get_mongodb_CTP(self):
        return self.__mongo_client.CTP

    # 从数据库获取user的strategy参数集合
    def get_col_strategy(self):
        return self.__mongo_client.CTP.get_collection(self.__user_id+'_strategy')

    # 从数据库获取user的持仓汇总集合
    def get_col_position(self):
        return self.__mongo_client.CTP.get_collection(self.__user_id+'_position')

    # 从数据库获取user的持仓明细集合
    def get_col_position_detail(self):
        return self.__mongo_client.CTP.get_collection(self.__user_id+'_position_detail')

    # 从数据库获取user的trade集合
    def get_col_trade(self):
        return self.__mongo_client.CTP.get_collection(self.__user_id+'_trade')

    # 从数据库获取user的order列表
    def get_col_order(self):
        return self.__mongo_client.CTP.get_collection(self.__user_id + '_order')

    # 获取期货账号
    def get_user_id(self):
        return self.__user_id

    # 获取交易员id
    def get_trader_id(self):
        return self.__trader_id

    # 获取trade实例(TD)
    def get_trade(self):
        return self.__trade

    # 获取self.__instrument_info
    def get_instrument_info(self):
        return self.__instrument_info

    # 设置user的交易开关，0关、1开
    def set_on_off(self, int_on_off):
        self.__on_off = int_on_off

    # 获取user的交易开关，0关、1开
    def get_on_off(self):
        return self.__on_off

    # 设置user初始化状态
    def set_init_finished(self, bool_input):
        self.__init_finished = bool_input

    # 获取user初始化状态
    def get_init_finished(self):
        return self.__init_finished

    # 获取交易日
    def GetTradingDay(self):
        return self.__TradingDay

    # 获取报单引用part2
    def add_order_ref_part2(self):
        self.__order_ref_part2 += 1
        return self.__order_ref_part2

    # 添加交易策略实例，到self.__list_strategy
    def add_strategy(self, obj_strategy):
        self.__list_strategy.append(obj_strategy)  # 将交易策略实例添加到本类的交易策略列表
        self.__trade.set_list_strategy(self.__list_strategy)  # 将本类的交易策略列表转发给trade
        obj_strategy.set_user(self)  # 将user设置为strategy属性

    # 添加合约代码到user类的self.__dict_instrument_action_counter
    def add_instrument_id_action_counter(self, list_instrument_id):
        for i in list_instrument_id:
            if i not in self.__dict_instrument_action_counter:
                self.__dict_instrument_action_counter[i] = 0

    # 撤单计数
    def action_counter(self, instrument_id):
        if instrument_id in self.__dict_instrument_action_counter:
            self.__dict_instrument_action_counter[instrument_id] += 1

    # 删除交易策略实例，从self.__list_strategy
    def del_strategy(self, strategy_id):
        for i in self.__list_strategy:
            if i.get_strategy_id() == strategy_id:
                self.__list_strategy.remove(i)

    # 获取list_strategy
    def get_list_strategy(self):
        return self.__list_strategy

    # 获取合约撤单次数的字典
    def get_dict_instrument_action_counter(self):
        return self.__dict_instrument_action_counter

    # 查询行情
    def qry_depth_market_data(self, instrument_id):
        return self.__trade.QryDepthMarketData(instrument_id)

    # 查询合约
    def qry_instrument(self):
        return self.__trade.QryInstrument()

    # 转PyCTP_Market_API类中回调函数OnRtnOrder
    def OnRtnTrade(self, Trade):
        # print("User.OnRtnTrade()", 'OrderRef:', Trade['OrderRef'], 'Trade:', Trade)
        t = datetime.datetime.now()
        Trade['OperatorID'] = self.__trader_id  # 客户端账号（也能区分用户身份或交易员身份）:OperatorID
        Trade['StrategyID'] = Trade['OrderRef'][-2:]  # 报单引用末两位是策略编号
        Trade['RecTradeTime'] = t.strftime("%Y-%m-%d %H:%M:%S")  # 收到成交回报的时间
        Trade['RecTradeMicrosecond'] = t.strftime("%f")  # 收到成交回报中的时间毫秒
        # self.__DBManager.insert_trade(Trade)  # 记录插入到数据库
        if self.__mongo_client is not None:
            self.__mongo_client.CTP.get_collection(self.__user_id.decode()+'_Trade').insert_one(Trade)  # 记录插入到数据库
        else:
            print("User.OnRtnTrade() self.__mongo_client is None")

    # 转PyCTP_Market_API类中回调函数OnRtnOrder
    def OnRtnOrder(self, Order):
        # print("User.OnRtnOrder()", 'OrderRef:', Order['OrderRef'], 'Order:', Order)
        t = datetime.datetime.now()
        Order['OperatorID'] = self.__trader_id  # 客户端账号（也能区分用户身份或交易员身份）:OperatorID
        Order['StrategyID'] = Order['OrderRef'][-2:]  # 报单引用末两位是策略编号
        Order['RecOrderTime'] = t.strftime("%Y-%m-%d %H:%M:%S")  # 收到成交回报的时间
        Order['RecOrderMicrosecond'] = t.strftime("%f")  # 收到成交回报中的时间毫秒
        # self.__DBManager.insert_trade(Order)  # 记录插入到数据库
        self.__mongo_client.CTP.get_collection(self.__user_id.decode()+'_Order').insert_one(Order)  # 记录插入到数据库

    """
    # 转PyCTP_Market_API类中回调函数OnRspQryTrade
    def OnRspQryTrade(self, Trade, RspInfo, RequestID, IsLast):
        self.__dfQryTrade = DataFrame.append(self.__dfQryTrade,
                                             other=Utils.code_transform(Trade),
                                             ignore_index=True)
        print("User.OnRspQryTrade() Trade =", Trade)
        print("User.OnRspQryTrade() RspInfo =", RspInfo)
        print("User.OnRspQryTrade() RequestID =", RequestID)
        print("User.OnRspQryTrade() IsLast =", IsLast)

    # 转PyCTP_Market_API类中回调函数OnRspQryOrder
    def OnRspQryOrder(self, Order, RspInfo, RequestID, IsLast):
        self.__dfQryOrder = DataFrame.append(self.__dfQryOrder,
                                             other=Utils.code_transform(Order),
                                             ignore_index=True)
        print("User.OnRspQryTrade() Order =", Order)
        print("User.OnRspQryTrade() RspInfo =", RspInfo)
        print("User.OnRspQryTrade() RequestID =", RequestID)
        print("User.OnRspQryTrade() IsLast =", IsLast)
    """

    # 转PyCTP_Market_API类中回调函数QryTrade
    def QryTrade(self):
        self.__listQryTrade = self.__trade.QryTrade()
        print("User.QryTrade() list_QryTrade =", self.__user_id, self.__listQryTrade)
        for i in self.__listQryTrade:
            self.__dfQryTrade = DataFrame.append(self.__dfQryTrade,
                                                 other=Utils.code_transform(i),
                                                 ignore_index=True)

    # 转PyCTP_Market_API类中回调函数QryOrder
    def QryOrder(self):
        self.__listQryOrder = self.__trade.QryOrder()
        print("User.QryOrder() list_QryOrder =", self.__user_id, self.__listQryOrder)
        for i in self.__listQryOrder:
            self.__dfQryOrder = DataFrame.append(self.__dfQryOrder,
                                                 other=Utils.code_transform(i),
                                                 ignore_index=True)

    # 获取listQryOrder
    def get_listQryOrder(self):
        return self.__listQryOrder

    # 获取listQryTrade
    def get_listQryTrade(self):
        return self.__listQryTrade

    # 获取dfQryOrder
    def get_dfQryOrder(self):
        return self.__dfQryOrder

    # 获取dfQryTrade
    def get_dfQryTrade(self):
        return self.__dfQryTrade


if __name__ == '__main__':
    print("User.py, if __name__ == '__main__':")
        


