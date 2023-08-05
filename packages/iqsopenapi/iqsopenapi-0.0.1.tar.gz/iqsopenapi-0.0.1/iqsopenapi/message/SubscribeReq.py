# -*- coding: utf-8 -*-
from iqsopenapi.message.IMessage import *

class SubscribeReq(RequestMessage):
    """订阅请求"""
    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.Subscribe

        """订阅列表"""
        self.Subscribes = []

    def ToDict(self):
        return {"RequestType":self.RequestType,"ReqID":self.ReqID,"Subscribes":self.Subscribes}

class SubscribeStgyReq(RequestMessage):
    """订阅请求"""
    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.Subscribe
        """量化Id"""
        self.StrategyKey=""

    def ToDict(self):
        return {"RequestType":self.RequestType,"ReqID":self.ReqID,"StrategyKey":self.StrategyKey}

