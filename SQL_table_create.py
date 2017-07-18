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
cursor.execute('create table doubanmovie_TOP250 '
               '(id int NOT NULL AUTO_INCREMENT,'
               '电影名称 varchar(255),'
               '年份 date,'
               '导演 varchar(255),'
               '编剧 varchar(255),'
               '主演 text,'
               '类型 varchar(255),'
               '制片国家 varchar(255),'
               '片长 varchar(255),'
               '评分 int,'
               '评价人数 int,'
               '5星 varchar(24),'
               '4星 varchar(24),'
               '3星 varchar(24),'
               '2星 varchar(24),'
               '1星 varchar(24),'
               '好于 varchar(255),'
               'primary key (id,电影名称))')
cursor.close()
conn.commit()
conn.close()
