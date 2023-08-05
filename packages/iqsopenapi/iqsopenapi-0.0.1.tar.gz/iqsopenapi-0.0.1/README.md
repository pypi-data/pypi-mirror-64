# -*- coding: utf-8 -*-
from iqsopenapi import *

if __name__ == '__main__':
    """≤‚ ‘"""
    try:
       api = StgyOpenApi("1",print,print,print,print,"d://logs/IQS.OpenApi.Python/")
       api.Start()           
       sub = api.Subscribe([{'symbol':'rb2005','exchange':4,'marketType':'TICK','barType':0},{'symbol':'rb2005','exchange':4,'marketType':'BAR','barType':60}])
       unSub = api.Unsubscribe([{'symbol':'rb2005','exchange':4,'marketType':'TICK','barType':60}])
       subList = api.GetSubscribeList()
       lastTick = api.GetLastTick("rb2005",Exchange.SHFE,1)
       lastBar = api.GetLastBar('rb2005',Exchange.SHFE,5 * 60,1)
       hisBar = api.GetHisBar('rb2005',Exchange.SHFE,5 * 60,20190101120000,20190101140000)
       clientOrderId = uuid.uuid4().hex
       sendOrder = api.SendOrder(clientOrderId,'rb2005',Exchange.SHFE,"B",2400,1,OrderType.MKT,Offset.Open,'≤‚ ‘')
       cancelOrder = api.CancelOrder("1231231")
       assetInfo = api.GetAssetInfo()
       orders = api.GetOrders()
       order = api.GetOrder(clientOrderId)
       openOrders = api.GetOpenOrders()   
       positions = api.GetPositions()
       contract = api.GetContract('rb2005',Exchange.SHFE)
    except Exception as e:
        print(e)
    pass


 

