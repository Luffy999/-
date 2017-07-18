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
cursor.execute('select title from 广西_南宁_青秀_政府办_政务动态 where title like "%美%京%"')
values = cursor.fetchall()
for i in values:
    print i[0]
cursor.close()
conn.commit()
conn.close()
