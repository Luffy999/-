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
# 导入数据
cursor.execute('insert into 邕宁食药局 (id,标题,时间,内容) values (%s,%s,%s,%s)',[2,'title','time','content'])
# 断开连接，并关闭数据库
cursor.close()
conn.commit()
conn.close()
