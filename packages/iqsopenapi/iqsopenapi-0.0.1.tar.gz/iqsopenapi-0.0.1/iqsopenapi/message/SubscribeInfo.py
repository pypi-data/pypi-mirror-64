# -*- coding: utf-8 -*- 
from iqsopenapi.models import *
from enum import IntEnum

class SubscribeInfo(object):
    """订阅消息"""

    def __init__(self):
        """合约代码"""
        self.Symbol = ""

        """合约代码"""
        self.Exchange = Exchange.UnKnow
        
        """行情类型"""
        self.MarketType = MarketType.UnKnow
        
        """周期类型 以秒为单位 5*60：5分钟线  60*60：小时线  24*60*60 日线"""
        self.BarType = 0
    
    def ToDict(self):
        return {"Symbol":self.Symbol,"Exchange":int(self.Exchange),"MarketType":int(self.MarketType),"BarType":self.BarType}

    def ToString(self):
        return "{0}.{1}.{2}.{3}".format(self.Symbol,str(self.Exchange.name).upper(),str(self.MarketType.name).upper(),self.BarType)

class MarketType(IntEnum):
    """行情类型"""

    """未知"""
    UnKnow = 0

    """逐笔数据"""
    TICK = 1

    """周期数据"""
    BAR = 2


