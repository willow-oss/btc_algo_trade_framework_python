 # -*- coding: utf-8 -*-
import json
import websocket
import datetime
from ws_base import WS_Base
import numpy as np

class BitMex_WS_Board(WS_Base):
    def __init__(self):                     
        WS_Base.__init__(self)
        #rows in mysql table
        ROWS = 5
        #Realtime-api information
        self.url = "wss://www.bitmex.com/realtime"
        self.ws = websocket.WebSocketApp(self.url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close)
        self.channels = json.dumps({
            'op': 'subscribe',
            'args': ["orderBook10:XBTUSD"]})

        #private mysql information    
        self.TBL_name = 'BitMex_WS_Board'
        self.columns_tuple_str = """(time, mid, board_sum1, board_sum2, board_sum3, board_sum4, board_sum5,
                              bid_ratio1, bid_ratio2, bid_ratio3, bid_ratio4, bid_ratio5)"""
        self.initialize_mysql_board_table(ROWS)
                    
    def on_message(self, message):
        #extracting data from message
        nowT = datetime.datetime.now()
        r = json.loads(message)["data"][0] 
        mid = 0
        bids = np.array(r["bids"])
        asks = np.array(r["asks"])    
        bid_sum1 = sum(bids[0:2,1])
        ask_sum1 = sum(asks[0:2,1])
        bid_sum2 = sum(bids[2:4,1])
        ask_sum2 = sum(asks[2:4,1])
        bid_sum3 = sum(bids[4:6,1])
        ask_sum3 = sum(asks[4:6,1])
        bid_sum4 = sum(bids[6:8,1])
        ask_sum4 = sum(asks[6:8,1])
        bid_sum5 = sum(bids[8:10,1])
        ask_sum5 = sum(asks[8:10,1])        
        board_sum1 = bid_sum1 + ask_sum1
        board_sum2 = bid_sum2 + ask_sum2
        board_sum3 = bid_sum3 + ask_sum3
        board_sum4 = bid_sum4 + ask_sum4
        board_sum5 = bid_sum5 + ask_sum5            
        bid_ratio1 = bid_sum1 / board_sum1
        bid_ratio2 = bid_sum2 / board_sum2
        bid_ratio3 = bid_sum3 / board_sum3
        bid_ratio4 = bid_sum4 / board_sum4
        bid_ratio5 = bid_sum5 / board_sum5

        val = (nowT, mid, board_sum1, board_sum2, board_sum3, board_sum4, board_sum5,
                              bid_ratio1, bid_ratio2, bid_ratio3, bid_ratio4, bid_ratio5)
        self.update_board_data_in_mysql(val)  
        

