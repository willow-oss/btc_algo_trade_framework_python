# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 20:19:53 2019

@author: willow-oss
"""

from bitflyer_fx_ws_board import BitFlyer_FX_WS_Board
from bitflyer_fx_ws_execution import BitFlyer_FX_WS_Execution
from bitflyer_ws_execution import BitFlyer_WS_Execution
import threading
import time

if __name__ == '__main__':
    
    #lag period(seconds) between each websocket objects
    TAU = 5
    
    bFFX_WS_E = BitFlyer_FX_WS_Execution()
    bFFX_WS_B = BitFlyer_FX_WS_Board()
    bF_WS_E = BitFlyer_WS_Execution()
    print("Initialization Completed.")
    
    
    thread1 = threading.Thread(target = bFFX_WS_E.job)
    time.sleep(TAU)
    thread2 = threading.Thread(target = bFFX_WS_B.job)
    time.sleep(TAU)
    thread3 = threading.Thread(target = bF_WS_E.job)
    
    thread1.start()
    time.sleep(5)
    thread2.start()
    time.sleep(5)
    thread3.start()


    