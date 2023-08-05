# -*- coding: utf-8 -*-
from iqsopenapi.message.IMessage import *

class UnsubscribeReq(RequestMessage):

    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.Unsubscribe

        """取消订阅列表"""
        self.Unsubscribes = []

    def ToDict(self):
        return {"ReqID":self.ReqID,"RequestType":self.RequestType,"Unsubscribes":self.Unsubscribes}