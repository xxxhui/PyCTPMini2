# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 00:31:14 2016

@author: Zhuolin
"""

import sys
import time
import os
import threading
import chardet
import pandas as pd
from pandas import Series, DataFrame
import FunctionLog
from Trade import PyCTP_Trader
from Market import PyCTP_Market
import Utils


def __main__():
    BrokerID = b'9999'
    UserID = b'063802'
    Password = b'123456'
    ExchangeID = b'SHFE'
    listInstrumentID = [b'cu1701', b'cu1612']
    InstrumentID = b'cu1701'
    trader = PyCTP_Trader.CreateFtdcTraderApi(b'tmp/_tmp_t_')  # Trade实例
    market = PyCTP_Market.CreateFtdcMdApi(b'tmp/_tmp_m_')  # Market实例
    print('连接交易前置', Utils.code_transform(trader.Connect(b'tcp://180.168.146.187:10000')))
    print('连接行情前置', Utils.code_transform(market.Connect(b'tcp://180.168.146.187:10010')))
    print('交易账号登陆', Utils.code_transform(trader.Login(BrokerID, UserID, Password)))
    print('交易账号登陆', Utils.code_transform(market.Login(BrokerID, UserID, Password)))
    print('交易日', Utils.code_transform(trader.GetTradingDay()))
    print('设置投资者代码', Utils.code_transform(trader.setInvestorID(UserID)))
    # time.sleep(1.0)
    # print('查询交易所', Utils.code_transform(trader.QryExchange()))
    # time.sleep(1.0)
    # print('查询投资者', Utils.code_transform(trader.QryInvestor()))
    # time.sleep(1.0)
    # print('查询资金账户', Utils.code_transform(trader.QryTradingAccount()))
    # time.sleep(1.0)
    # print('查询合约', Utils.code_transform(trader.QryInstrument(b'SHFE')))
    # time.sleep(1.0)
    # dfInstrument.to_csv('data/dfInstrument.csv')
    # time.sleep(1.0)
    # print('查询交易代码', Utils.code_transform(trader.QryTradingCode(ExchangeID)))
    # time.sleep(1.0)
    # print('合约手续费率', Utils.code_transform(trader.QryInstrumentCommissionRate(InstrumentID)))
    # time.sleep(1.0)
    # print('合约保证金率', Utils.code_transform(trader.QryInstrumentMarginRate(InstrumentID)))
    # time.sleep(1.0)
    # print('查询报单', Utils.code_transform(trader.QryOrder()))
    # time.sleep(1.0)
    # print('查询成交单', Utils.code_transform(trader.QryTrade()))
    # time.sleep(1.0)
    # print('投资者持仓', Utils.code_transform(trader.QryInvestorPosition()))
    # time.sleep(1.0)
    # print('查询行情', Utils.code_transform(trader.QryDepthMarketData(InstrumentID)))
    # time.sleep(1.0)
    # print('订阅行情', Utils.code_transform(market.SubMarketData(listInstrumentID)))

    # 调试OrderInsert
    while True:
        Utils.print_menu()
        var = input()

        if var == 'e':
            print('查询交易所信息\n', Utils.code_transform(trader.QryExchange()))
            continue

        if var == 's':
            print('请选择要查询的交易所合约信息：\ns = 上海期货交易所\nd = 大连商品交易所\nz = 郑州商品交易所\nc = 中国金融期货交易所\na=以上所有交易所')
            var = input()
            if var == 's':
                input_params = b'SHFE'
            elif var == 'd':
                input_params = b'DCE'
            elif var == 'z':
                input_params = b'CZCE'
            elif var == 'c':
                input_params = b'CFFEX'
            elif var == 'a':
                input_params = b''
            else:
                print('输入错误')
                continue
            print('查询合约', Utils.code_transform(trader.QryInstrument(input_params)))
            continue

        if var == 'u':
            print('查询账户信息\n', Utils.code_transform(trader.QryInvestor()))
            continue

        if var == 't':
            print('查询账户资金\n', Utils.code_transform(trader.QryTradingAccount()))
            continue

        if var == 'h':
            print('查询账户持仓汇总\n', Utils.code_transform(trader.QryInvestorPosition()))
            continue

        if var == 'H':
            print('查询账户持仓明细\n', Utils.code_transform(trader.QryInvestorPositionDetail()))
            continue

        if var == 'o':
            print('查询委托记录\n', Utils.code_transform(trader.QryOrder()))
            continue

        if var == 'd':
            print('查询交易记录\n', Utils.code_transform(trader.QryTrade()))
            continue

        if var == 'i':
            print('please input OrderInsert arguments dict:\n')
            input_params = input()
            try:
                input_params = eval(input_params)
            except SyntaxError as e:
                print('except:', e)
                print('输入参数错误')
                continue
            print('输入参数为\n', input_params)
            trader.OrderInsert(InstrumentID=input_params['InstrumentID'],
                               Action=input_params['Action'],
                               Direction=input_params['Direction'],
                               Volume=input_params['Volume'],
                               Price=input_params['Price'],
                               OrderRef=input_params['OrderRef'])
            continue

        # 进入OrderAction命令模式
        if var == 'a':
            print('please input OrderAction arguments:\n')
            input_params = input()
            try:
                input_params = eval(input_params)
            except SyntaxError as e:
                print('except:', e)
                print('输入参数错误')
                continue
            print('输入参数为\n', input_params)
            trader.OrderAction(ExchangeID=input_params['ExchangeID'],
                               OrderRef=input_params['OrderRef'],
                               OrderSysID=input_params['OrderSysID'])
            continue

        # 退出
        if var == 'b':
            break

        # 保存文件到本地
        if var == 'l':
            path_tmp = 'data/'+trader.get_UserID().decode()+'_Tick.csv'
            PyCTP_Market.df_data.to_csv(path_tmp)  # 保存行情到本地csv文件
            path_tmp = 'data/'+trader.get_UserID().decode()+'_Instrument.csv'
            PyCTP_Trader.dfInstrument.to_csv(path_tmp)  # 保存合约状态到本地csv文件
            path_tmp = 'data/'+trader.get_UserID().decode()+'_Postion.csv'
            PyCTP_Trader.dfQryInvestorPosition.to_csv(path_tmp)  # 保存持仓到本地csv文件
            path_tmp = 'data/'+trader.get_UserID().decode()+'_PostionDetail.csv'
            PyCTP_Trader.dfQryInvestorPositionDetail.to_csv(path_tmp)  # 保存持仓明细到本地csv文件
            path_tmp = 'data/'+trader.get_UserID().decode()+'_RecordOrder.csv'
            PyCTP_Trader.dfRecordOrder.to_csv(path_tmp)  # 保存Trade回调记录到本地csv文件
            path_tmp = 'data/'+trader.get_UserID().decode()+'_RecordTrade.csv'
            PyCTP_Trader.dfRecordTrade.to_csv(path_tmp)  # 保存Order回调记录到本地csv文件
            continue

        # 输入错误重新输入
        if True:
            print('input error, please input again\n')
            continue
            # 保存数据到本地

    time.sleep(1.0)
    print('退订行情:', market.UnSubMarketData(listInstrumentID))
    print('交易账号登出', trader.Logout())
    print('行情账号登出', market.Logout())


if __name__ == '__main__':
    __main__()

