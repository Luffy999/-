# -*- coding:utf-8 -*-
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='luffy',
    password='123456',
    database='movie',
)
cursor = conn.cursor()
cursor.execute('create table lagou_jobs_python数据 '
               '(id int NOT NULL AUTO_INCREMENT,'
               '公司 varchar(255),'
               '职位 varchar(255),'
               '薪资 varchar(255),'
               '城市 varchar(4),'
               '经验 varchar(255),'
               '学历 varchar(255),'
               '全兼职 varchar(255),'
               '标签 varchar(255),'
               '职位诱惑 varchar(255),'
               '职位描述 text,'
               '工作地址 varchar(255),'
               'primary key (id))')
cursor.close()
conn.commit()
conn.close()