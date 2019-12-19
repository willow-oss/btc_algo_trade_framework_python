 # -*- coding: utf-8 -*-
import json
import websocket
import datetime
from ws_base import WS_Base

class BitMex_WS_Execution(WS_Base):
    def __init__(self):                     
        WS_Base.__init__(self)
        #rows in mysql table
        ROWS = 200        
        #Realtime-api information    
        self.url = "wss://www.bitmex.com/realtime"
        self.ws = websocket.WebSocketApp(self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        self.channels = json.dumps({
            'op': 'subscribe',
            'args': ["trade:XBTUSD"]})
    
        #private mysql information     
        self.TBL_name = 'BitMex_WS_Execution'
        self.columns_tuple_str = "(time,timestamp,ltp,side,size)"
        self.initialize_mysql_excution_table(ROWS)
                    
    def on_message(self, message):        
        #extracting data from message
        r = json.loads(message)["data"][0]
        ltp = r["price"]
        side = r["side"]
        size = r["size"]
        nowT = datetime.datetime.now()
        res_time = r["timestamp"].replace('T', ' ')[:-1]
        res_time = datetime.datetime(int(res_time[:4]), int(res_time[5:7]), int(res_time[8:10]), int(res_time[11:13]), int(res_time[14:16]), int(res_time[17:19]), int(res_time[20:-1]))
        
        val = (nowT, res_time, ltp, side, size)
        self.update_execution_data_in_mysql(val)
        

