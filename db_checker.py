# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:37:53 2020

@author: ConorG
"""
import sqlite3

def check_sql_lite_table():
    conn = sqlite3.connect('active_customers.db') 
    mycur = conn.cursor()
    mycur.execute("SELECT * FROM ACTIVE_CUSTOMERS")
    print(mycur.fetchall())

if __name__ == '__main__':
    check_sql_lite_table()
