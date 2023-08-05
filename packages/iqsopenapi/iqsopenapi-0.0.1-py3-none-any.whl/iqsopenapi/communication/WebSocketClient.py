# -*- coding: utf-8 -*-
from iqsopenapi.util.MemCache import *
from websocket import create_connection
from iqsopenapi.message.IMessage import *
from iqsopenapi.message.ReplyResp import *
from iqsopenapi.message.HeartBeatReq import *
from queue import Queue
import socket
import asyncio
import datetime
import threading
import time
import sys
import uuid
import json

class WebSocketClient(object):
    """WebSocket"""

    #超时时间
    __Timeout = 30
    #单条消息终结符
    __EOL = 10

    def __init__(self,url,heartBeatInternal,keepAliveTimeout,recvFn,errorFn):
        """构造函数"""

        #连接地址
        self.url = url
        #发送心跳的时间间隔
        self.heartBeatInternal = heartBeatInternal
        #心跳超时时间
        self.keepAliveTimeout = keepAliveTimeout
        #websocket
        self.client = None
        #上次活跃时间
        self.lastActiveTime = datetime.datetime.now()
        self.__recvFn = recvFn
        self.__errorFn = errorFn
        self.__unhandledQueue = Queue()
        self.__responseMsgCache = MemCache()
        t = threading.Thread(target=self.__TimerHandleMsg)
        t.start()
        t1 = threading.Thread(target=self.__TimerAutoHeartBeat)
        t1.start()
    
    def Connect(self):
        """连接"""
        if self.__IsAvaliable(self.client):
            return True
        self.__wirteInfo("uri:{0},开始连接".format(self.url))
        self.client = create_connection(self.url)
        self.__wirteInfo("uri:{0},连接成功,state:{1}".format(self.url,self.client.connected))
        self.lastActiveTime = datetime.datetime.now()
        t = threading.Thread(target=self.__TimerReceiveMsg)
        t.start()
        return True

    def IsConnected(self):
        """判断是否连接"""
        if not self.client:
            return False
        return self.client.connected

    def __IsAvaliable(self,client):
        """判断是否是有效连接"""
        if not client:
            return False
        return client.connected

    def Send(self,request):
        """发送消息"""
        if not request or not self.client:
            return None
        request["ReqID"] = uuid.uuid1().hex
        message = json.dumps(request,ensure_ascii=False)
        self.client.send(message)
        i = 0
        while i < self.__Timeout:
            reply = self.__responseMsgCache.get(request["ReqID"])
            if reply:
              return reply
            i += 1
            time.sleep(1)
        return None
 
    def __TimerReceiveMsg(self):
        """接收消息"""
        while self.__IsAvaliable(self.client):
            try:
                 if not self.client:
                     time.sleep(3)
                     continue
                 result = self.client.recv()
                 self.lastActiveTime = datetime.datetime.now()
                 self.__unhandledQueue.put(result)
            except Exception as e:
                self.__errorFn(e)
                if self.client:
                  self.client.close()
                self.client = None
                time.sleep(3)
        if not self.client:
            return
        self.client.close()

    def __TimerHandleMsg(self):
        """处理消息"""
        while True:
            try:
                msg = self.__unhandledQueue.get()
                if not msg:
                    time.sleep(10)
                    continue
                self.__RaiseMessage(msg)
            except Exception as e:
                self.__errorFn(e)
                time.sleep(10)
    
    def __TimerAutoHeartBeat(self):
        """心跳"""
        req = HeartBeatReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.HeartBeat
        obj = req.ToDict()
        message = json.dumps(obj,ensure_ascii=False)
        self.__wirteInfo("启动心跳发送线程")
        while True:
            time.sleep(self.heartBeatInternal)
            try:
                if not self.__IsAvaliable(self.client):
                    self.__wirteInfo("心跳检测时连接已断开:{0}".format(self.url))
                    continue
                if(datetime.datetime.now() - self.lastActiveTime).seconds > self.keepAliveTimeout:
                    self.client.close()
                    self.client = None
                    self.__wirteError("心跳监测超时，释放连接：{0}".format(self.url))
                    continue
                self.client.send(message)
                self.__wirteInfo("发送一次心跳:{0}".format(self.url))
            except Exception as e:
                self.__errorFn(e)

    def __RaiseMessage(self,msg):
        if not msg:
            return
        data = json.loads(msg,encoding='utf-8')
        responseType = data.get("rt")
        if responseType == ResponseType.HeartBeat.name:
            self.__wirteInfo("收到一次心跳:{0}".format(self.url))
            return
        if responseType == ResponseType.Reply.name:
            self.__responseMsgCache.set(data.get("ReqID"),data,60 * 5)
            return
        if responseType == ResponseType.TickData.name:
            self.__recvFn(data)
            return
        if responseType == ResponseType.KlineData.name:
            self.__recvFn(data)
            return
        if responseType == ResponseType.OrderChange.name:
            self.__recvFn(data)
            return
        if responseType == ResponseType.OrderExec.name:
            self.__recvFn(data)
            return
        return 

    def WriteLog(self,fileName, log):
        """写日志"""
        LogRecord.writeLog(fileName,log)

    def __wirteError(self,error):
        '''写错误日志'''
        self.WriteLog('WebSocketClientError',error)

    def __wirteInfo(self,info,isPrint=True):
        '''写日志'''
        LogRecord.writeLog('WebSocketClient',info,isPrint)
         
        