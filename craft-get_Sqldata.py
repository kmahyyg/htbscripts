#!/usr/bin/python

import pymysql

DB_USER = 'craft'
DB_PASSWD = 'qLGockJ6G2J75O'
DB_DB = 'craft'
DB_HOST = 'db'

connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWD, charset='utf8', db=DB_DB, cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        #Part 1: sql1 = "show tables;"
        #sql2 = "show databases;"
        #Error: sql3 = "use mysql; select * from user;"
        #Part 2: 
        sql1 = "select * from user;"
        #8.0.15: sql2 = "select @@version;"
        #sql3 = "SELECT schema_name FROM information_schema.schemata;"
        #Part 3: sql1 = "select * from information_schema.user_privileges;"
        # sql2 = "select * from information_schema.tables;"
        #Error: sql3 = "use information_schema; show tables;"
        cursor.execute(sql1)
        print(cursor.fetchall())
        #cursor.execute(sql2)
        #print(cursor.fetchall())
        #cursor.execute(sql3)
        #print(cursor.fetchall())
except:
    print("error detected")
finally:
    connection.close()

