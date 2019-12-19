 # -*- coding: utf-8 -*-
import websocket
import time
import mysql.connector

class WS_Base():
    def __init__(self):                     
        self.connect = mysql.connector.connect(user='hogehoge', 
                                               password='hogehoge', 
                                               host='hogehost', 
                                               database='hogeDB', 
                                               charset='utf8')
        self.cursor = self.connect.cursor()
    
    def on_message(self, message):
        pass
        
    def on_error(self, error):
        self.disconnect()
        time.sleep(0.5)
        self.connect()
    
    def on_close(self):
        while True:
            time.sleep(10)
            try:
                self.ws = websocket.WebSocketApp(self.url,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close)
                self.ws.on_open = self.on_open
                self.ws.run_forever()
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
    
    def initialize_mysql_excution_table(self, ROWS):
        #drop past table
        self.cursor.execute("DROP TABLE IF EXISTS " + self.TBL_name)
        
        #create a new table
        self.cursor.execute("CREATE TABLE " + self.TBL_name + """
                       ( time datetime,
                       timestamp datetime,
                       ltp float,
                       side varchar(5),
                       size float)""")
        
        #insert dummy data
        nowT = "2019-12-12 18:29:25.269995"
        res_time = "2019-12-12 18:29:25.269995"
        ltp = 1000000.00
        size = 0.01
        side = "buy"
        insert_sql = ('insert into ' + self.TBL_name + ' ' + self.columns_tuple_str + ' values (%s, %s, %s, %s, %s);')
        val = (nowT, res_time, ltp, side, size)
        for i in range(ROWS):
            self.cursor.execute(insert_sql, val)
        self.connect.commit()
        print(self.TBL_name + " initialization completed.")
    
    def initialize_mysql_board_table(self, ROWS):
        #drop past table
        self.cursor.execute("DROP TABLE IF EXISTS " + self.TBL_name)

        #create a new table
        self.cursor.execute("CREATE TABLE IF NOT EXISTS " + self.TBL_name + """
                       ( time datetime,
                       mid float,
                       board_sum1 float, 
                       board_sum2 float, 
                       board_sum3 float, 
                       board_sum4 float, 
                       board_sum5 float,
                       bid_ratio1 float, 
                       bid_ratio2 float, 
                       bid_ratio3 float, 
                       bid_ratio4 float, 
                       bid_ratio5 float)""")
        #insert dummy data
        nowT ="2019-12-12 18:29:25.269995"
        mid = 1000000
        board_sum1 = 1
        board_sum2 = 1
        board_sum3 = 1
        board_sum4 = 1
        board_sum5 = 1
        bid_ratio1 = 0.5
        bid_ratio2 = 0.5
        bid_ratio3 = 0.5
        bid_ratio4 = 0.5
        bid_ratio5 = 0.5
        insert_sql = ('insert into ' + self.TBL_name + ' ' + self.columns_tuple_str + ''' values (%s,%s, %s, %s, %s, %s, 
                                                                                                  %s, %s, %s, %s, %s, %s);''')
        val = (nowT, mid, board_sum1, board_sum2, board_sum3, board_sum4, board_sum5,
                              bid_ratio1, bid_ratio2, bid_ratio3, bid_ratio4, bid_ratio5)
        for i in range(ROWS):
            self.cursor.execute(insert_sql, val)        
        self.connect.commit()  
        print(self.TBL_name + " initialization completed.")
        
    def update_execution_data_in_mysql(self, val):
        #insert new data to mysql table
        insert_sql = ('insert into ' + self.TBL_name + ' ' + self.columns_tuple_str + ' values (%s, %s, %s, %s, %s);')
        self.cursor.execute(insert_sql, val)
        #deleting old data from mysql table
        delete_sql = ("delete from " + self.TBL_name + " order by time asc limit 1;")
        self.cursor.execute(delete_sql)  
        self.connect.commit()
        print("table "+ self.TBL_name + "updated.")
    
    def update_board_data_in_mysql(self, val):
        #inserting new data to mysql table
        insert_sql = ('insert into ' + self.TBL_name + ' ' + self.columns_tuple_str + ''' values (%s,%s, %s, %s, %s, %s, 
                                                                                                  %s, %s, %s, %s, %s, %s);''')
        self.cursor.execute(insert_sql, val)
        #deleting old data from mysql table
        delete_sql = ("delete from " + self.TBL_name + " order by time asc limit 1;")
        self.cursor.execute(delete_sql)  
        self.connect.commit()
        print("table "+ self.TBL_name + "updated.")    
    