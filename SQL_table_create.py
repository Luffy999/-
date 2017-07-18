# -*- coding:utf-8 -*-
# ------------------------------------------------------
#   版本：py2.7
#   日期：2017-06-23
#   作者：Luffy
# ------------------------------------------------------

import mysql.connector

# 连接数据库
conn = mysql.connector.connect(
    host='localhost',# 服务器名
    port=3306,# 端口
    user='******',# 用户名
    password='******',# 密码
    database='******',# 数据库名
)
cursor = conn.cursor()
# 设置字段属性
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
# 断开连接，并关闭数据库
cursor.close()
conn.commit()
conn.close()
