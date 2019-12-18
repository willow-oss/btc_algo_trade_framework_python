 # -*- coding: utf-8 -*-
import websocket
import time

class WS_Base():
    def __init__(self):                     
        pass
    
    def on_message(ws, message):
        pass
        
    def on_error(self, ws, error):
        self.disconnect()
        time.sleep(0.5)
        self.connect()
    
    def on_close(self, ws):
        while True:
            time.sleep(10)
            try:
                ws = websocket.WebSocketApp(self.url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close)
                ws.on_open = self.on_open
                ws.run_forever()
            except Exception:
                time.sleep(10)
        
    def on_open(self):
        print("### open ###")
        self.ws.send((self.channels))
        print("opened")
        
    def job(self):
        self.ws.on_open = self.on_open
        print("start job")
        self.ws.run_forever()
