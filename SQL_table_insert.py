# -*- coding:utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='******',
    password='******',
    database='******',
)
cursor = conn.cursor()
cursor.execute('insert into 邕宁食药局 (id,标题,时间,内容) values (%s,%s,%s,%s)',[2,'title','time','content'])
cursor.close()
conn.commit()
conn.close()
