# -*- coding: utf-8 -*-
from iqsopenapi.util.HttpHelper import *
from iqsopenapi.util.LogRecord import *
from iqsopenapi.models.Contract import *
from iqsopenapi.models.TickData import *
from iqsopenapi.models.KlineData import *
from iqsopenapi.util.DES3Cryptogram import *
from iqsopenapi.communication.WebSocketClient import *
from iqsopenapi.marketdata.IMarketApi import *
from iqsopenapi.message.IMessage import *
from iqsopenapi.message.SubscribeReq import *
from iqsopenapi.message.UnsubscribeReq import *
from iqsopenapi.models.BarData import *
import json
import time
import uuid
import iqsopenapi.util.LogRecord
import datetime
import traceback
import threading

class MarketApi(IMarketApi):
    """行情接口"""

    #自动重连检测时间
    AutoReconnectInterval = 10

    #发送心跳的时间间隔
    heartBeatInternal = 5

    #心跳超时时间
    keepAliveTimeout = 30

    def __init__(self,connectionUrl,apiHost,tickCallback,barCallback):
        """构造函数"""
        super(MarketApi,self).__init__(connectionUrl,apiHost,tickCallback,barCallback)
        self._apiHost=apiHost
        self.__tickCallback = tickCallback
        self.__barCallback = barCallback
        self.__client = WebSocketClient(connectionUrl,self.heartBeatInternal,self.keepAliveTimeout,self.__OnRecv,self.__OnError)
        self.__client.Connect()

    def Init(self):
        """初始化"""
        t = threading.Thread(target=self.__AuotReconnect,args=(self.__client,))
        t.start()
        return True

    def __AuotReconnect(self,client):
        """自动连接"""
        self.__wirteInfo("启动自动连接")
        while True:
            try:
                if not client.IsConnected():
                    self.__wirteInfo("未连接，尝试连接...")
                    ret = client.Connect()
                    self.__wirteInfo("重连完成：{0}".format(ret))
            except Exception as e:
                self.__wirteError("重连失败")
            time.sleep(self.AutoReconnectInterval)

    def __OnRecv(self,msg):
        '''收到行情消息'''
        if not msg:
            return
        type = msg.get("rt")
        if type == ResponseType.TickData.name:
            ticks = msg.get("Data")
            for item in ticks:
                tick = self.__ToTickData(item)
                if not tick:
                    return
                if self.__tickCallback:
                    self.__tickCallback(tick)
        if type == ResponseType.KlineData.name:
            bars = msg.get("Data")
            for item in bars:
                bar = self.__ToKlineData(item)
                if not bar:
                    return
                if self.__barCallback:
                    self.__barCallback(bar)

    def __ToKlineData(self,bar):
        #消息长度可能会增加
        if not bar:
            return None
        klineData = KlineData()
        klineData.Symbol = bar.get("s")
        klineData.Exchange = Exchange[bar.get("e")]
        klineData.DataType = int(bar.get("d"))
        klineData.LocalTime = datetime.datetime.strptime(bar.get("t"),'%Y%m%d%H%M%S') 
        klineData.PreClosePx = float(bar.get("pc"))
        klineData.OpenPx = float(bar.get("o"))
        klineData.HighPx = float(bar.get("h"))
        klineData.LowPx = float(bar.get("l"))
        klineData.ClosePx = float(bar.get("c"))
        klineData.Volume = int(bar.get("v"))
        klineData.Amount = int(bar.get("a"))
        klineData.OpenInterest = int(bar.get("oi"))
        klineData.SettlementPx = int(bar.get("sp"))
        return klineData

    def __ToTickData(self,tick):
        if not tick:
            return None
        tick = TickData()
        tick.Symbol = tick.get("s")
        tick.Exchange = Exchange[bar.get("e")]
        tick.LocalTime = datetime.datetime.strptime(tick.get("t"),'%Y%m%d%H%M%S') 
        tick.LastPx = float(tick.get("px"))
        tick.OpenPx = float(tick.get("o"))
        tick.HighPx = float(tick.get("h"))
        tick.LowPx = float(tick.get("l"))
        tick.UpLimitPx = float(tick.get("up"))
        tick.DownLimitPx = float(tick.get("dw"))
        tick.PreClosePx = float(tick.get("pc"))
        tick.Volume = int(tick.get("v"))
        tick.OpenInterest = int(tick.get("oi"))
        tick.SettlementPx = int(tick.get("sp"))
        bids = tick.get("bid")
        for x in bids:
            unit = LevelUnit()
            unit.Px = float(x['p'])
            unit.Vol = int(x['v'])
            tick.Bids.append(unit)
        asks = tick.get("ask")
        for x in asks:
            unit = LevelUnit()
            unit.Px = float(x['p'])
            unit.Vol = int(x['v'])
            tick.Asks.append(unit)
        return tick

    def __OnError(self,excp):
        '''发生错误时触发'''
        if not excp:
            return
        log = str(excp)
        log += traceback.format_exc()
        self.__wirteError(log)

    def GetStatus(self):
        """状态 -1:未初始化 1:正常 0:已断开"""
        if self.__client:
            return 1
        return -1

    def Subscribe(self,subInfos, isClear, isPlayback):
        """行情订阅"""
        if not self.__client:
            self.__wirteError('行情未初始化')
            return False
        if not subInfos:
            self.__wirteError('订阅参数不能为空')
            return False
        req = SubscribeReq()
        req.ReqID = uuid.uuid4().hex
        req.RequestType = RequestType.Subscribe
        req.Subscribes = subInfos
        obj = req.ToDict()
        if not self.__client.Send(obj):
            self.__wirteError("订阅消息发送失败")
            return False
        return True

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        if not self.__client:
            self.__wirteError('行情未初始化')
            return False
        if not subInfos:
            self.__wirteError('订阅参数不能为空')
            return False
        req = UnsubscribeReq()
        req.ReqID = uuid.uuid4().hex
        req.RequestType = RequestType.Unsubscribe
        req.Unsubscribes = subInfos
        obj = req.ToDict()
        if not self.__client.Send(obj):
            self.__wirteError("取消订阅消息发送失败")
            return False
        return True

    def GetHisBar(self,symbol, exchange, barType, startTime,endTime):
        """获取历史K线数据"""
        if not symbol:
            self.__wirteError("合约代码不能为空")
            return None
        klineType = self.__ToKlineType(barType)
        if not klineType:
            self.__wirteError("不支持的BarType：" + klineType)
            return None
        url = self._apiHost + 'MarketData/GetHisBar'
        params = {'symbol':symbol,'exchange':exchange,'dataType':klineType,'begin':startTime,'end':endTime}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            self.__wirteError("data为空：" + url + "," + strParams + "response：" + resp)
            return None
        result = []
        for x in data:
            bar = BarData()
            bar.Symbol = symbol
            bar.Exchange = exchange
            bar.DataType = dataType
            bar.LocalTime = datetime.datetime.strptime(x['timeStamp'],'%Y%m%d%H%M%S')
            bar.PreClosePx = abs(float(x['pc']))
            bar.OpenPx = abs(float(x['o']))
            bar.HighPx = abs(float(x['h']))
            bar.LowPx = abs(float(x['low']))
            bar.ClosePx = abs(float(x['c']))
            bar.Volume = int(x['v'])
            bar.Amount = int(x['a'])
            bar.OpenInterest = int(x['oi'])
            bar.SettlementPx = int(x['sp'])
            result.append(bar)
        return result

    def __ToKlineType(self,barType):
        '''转化为内部类型'''
        if barType == 60:
            return 1
        elif barType == 5 * 60:
            return 2
        elif barType == 15 * 60:
            return 3
        elif barType == 30 * 60:
            return 4
        elif barType == 60 * 60:
            return 5
        elif barType == 24 * 60 * 60:
            return 6
        elif barType == 7 * 24 * 60 * 60:
            return 7
        elif barType == 30 * 24 * 60 * 60:
            return 8
        elif barType == 365 * 24 * 60 * 60:
            return 9
        return None

    def __wirteError(self,error):
        '''写错误日志'''
        LogRecord.writeLog('MarketApiError',error)

    def __wirteInfo(self,info):
        '''写日志'''
        LogRecord.writeLog('MarketApi',info)
