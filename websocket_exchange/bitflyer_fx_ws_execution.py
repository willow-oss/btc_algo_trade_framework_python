 # -*- coding: utf-8 -*-
import json
import websocket
import datetime
from ws_base import WS_Base

class BitFlyer_FX_WS_Execution(WS_Base):
    def __init__(self):
        WS_Base.__init__(self)
        #rows in mysql table
        ROWS = 200
        #Realtime-api information
        self.url = "wss://ws.lightstream.bitflyer.com/json-rpc"
        self.ws = websocket.WebSocketApp(self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        self.channels = json.dumps({
                'method': 'subscribe',
                'params': {'channel': 'lightning_executions_FX_BTC_JPY'},})
    
        #private mysql information
        self.TBL_name = "bitFlyer_FX_WS_Execution"
        self.columns_tuple_str = "(time,timestamp,ltp,side,size)"

        self.initialize_mysql_excution_table(ROWS)
        
    def on_message(self, message):
        #extracting data from message
        r = json.loads(message)['params']['message'][0]
        nowT = datetime.datetime.now()
        res_time = r["exec_date"].replace('T', ' ')[:-1]
        res_time = datetime.datetime(int(res_time[:4]), int(res_time[5:7]), int(res_time[8:10]), int(res_time[11:13]), int(res_time[14:16]), int(res_time[17:19]), int(res_time[20:-1]))
        ltp = r["price"]
        size = r["size"]
        side = r["side"]
        val = (nowT, res_time, ltp, side, size)
        self.update_execution_data_in_mysql(val)
        