# -*- coding:utf-8 -*-
from email.mime.text import MIMEText
import time

# 输入Email地址和口令:
from_addr = '******'
password = '******'
# 输入SMTP服务器地址:
smtp_server = '******'
# 输入收件人地址:
to_addr = ['******']
msg = MIMEText('hello, send by Python...内容', 'plain', 'utf-8')
msg['Subject'] = time.ctime()
msg['From'] = u"机票价格爬虫" + "<" + from_addr + ">"
msg['To'] = ";".join(to_addr)


import smtplib
server = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())
server.quit()
