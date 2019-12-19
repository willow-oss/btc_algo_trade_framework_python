# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 20:19:53 2019

@author: willow-oss
"""

from bitmex_ws_execution import BitMex_WS_Execution
from bitmex_ws_board import BitMex_WS_Board
import threading
import time

if __name__ == '__main__':
    BM_WS_E = BitMex_WS_Execution()
    BM_WS_B = BitMex_WS_Board()
    print("Initialization Completed.")
    
    #lag period(seconds) between each websocket objects
    TAU = 5
    
    thread1 = threading.Thread(target = BM_WS_E.job)
    thread2 = threading.Thread(target = BM_WS_B.job)
    
    thread1.start()
    time.sleep(TAU)
    thread2.start()

    