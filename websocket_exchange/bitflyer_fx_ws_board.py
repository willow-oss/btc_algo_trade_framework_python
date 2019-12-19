 # -*- coding: utf-8 -*-
import json
import websocket
from ws_base import WS_Base
import datetime 

class BitFlyer_FX_WS_Board(WS_Base):
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
                'params': {'channel': 'lightning_board_FX_BTC_JPY'},})

        #private mysql information        
        self.TBL_name = 'bitFlyer_FX_WS_Board'
        self.columns_tuple_str = """(time, mid, board_sum1, board_sum2, board_sum3, board_sum4, board_sum5,
                              bid_ratio1, bid_ratio2, bid_ratio3, bid_ratio4, bid_ratio5)"""
        
        #create a virtual board
        self.bid_board = [0] * 2000000
        self.ask_board = [0] * 2000000
        self.initialize_mysql_board_table(ROWS)
        
    def on_message(self, message):
        #extracting data from message
        r = json.loads(message)['params']['message']
        nowT = datetime.datetime.now()
        mid = int(r["mid_price"])
        bid_update = r["bids"]
        ask_update = r["asks"]
        thresh1 = 500
        thresh2 = thresh1 * 2
        thresh3 = thresh2 * 2
        thresh4 = thresh3 * 2
        thresh5 = thresh4 * 2
        
        #updating the virtual board
        for i in range(len(bid_update)):
            self.bid_board[int(bid_update[i]["price"])] = float(bid_update[i]["size"])
        for i in range(len(ask_update)):
            self.ask_board[int(ask_update[i]["price"])] = float(ask_update[i]["size"])
        bid_sum1 = sum(self.bid_board[mid - thresh1 : mid])
        ask_sum1 = sum(self.ask_board[mid : mid + thresh1])
        bid_sum2 = sum(self.bid_board[mid - thresh2 : mid])
        ask_sum2 = sum(self.ask_board[mid : mid + thresh2])
        bid_sum3 = sum(self.bid_board[mid - thresh3 : mid])
        ask_sum3 = sum(self.ask_board[mid : mid + thresh3])
        bid_sum4 = sum(self.bid_board[mid - thresh4 : mid])
        ask_sum4 = sum(self.ask_board[mid : mid + thresh4])
        bid_sum5 = sum(self.bid_board[mid - thresh5 : mid])
        ask_sum5 = sum(self.ask_board[mid : mid + thresh5])
        
        #calculate the recording features (sum and ratio)
        board_sum1 = bid_sum1 + ask_sum1
        bid_ratio1 = bid_sum1 / board_sum1
        board_sum2 = bid_sum2 + ask_sum2
        bid_ratio2 = bid_sum2 / board_sum2
        board_sum3 = bid_sum3 + ask_sum3
        bid_ratio3 = bid_sum3 / board_sum3
        board_sum4 = bid_sum4 + ask_sum4
        bid_ratio4 = bid_sum4 / board_sum4
        board_sum5 = bid_sum5 + ask_sum5
        bid_ratio5 = bid_sum5 / board_sum5        
        val = (nowT, mid, board_sum1, board_sum2, board_sum3, board_sum4, board_sum5,
                              bid_ratio1, bid_ratio2, bid_ratio3, bid_ratio4, bid_ratio5)

        self.update_board_data_in_mysql(val)