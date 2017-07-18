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
# 查询
cursor.execute('select title from 广西_南宁_青秀_政府办_政务动态 where title like "%美%京%"')
values = cursor.fetchall()
for i in values:
    print i[0]
# 断开连接，并关闭数据库
cursor.close()
conn.commit()
conn.close()
