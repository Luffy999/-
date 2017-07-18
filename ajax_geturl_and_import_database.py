# -*- coding:utf-8 -*-
# ------------------------------------------------------
#   版本：py2.7
#   日期：2017-06-23
#   作者：Luffy
# ------------------------------------------------------

from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
import requests
import re
import traceback

# 使用无头浏览器获取URL
def url_get(page_down,page,URLnumber,url):
    # 启动无头浏览器
    driver = webdriver.Chrome(executable_path='******') # 浏览器名称和路径
    driver.get(url)
    # 路径搜索不到时需要定位frame
    # driver.switch_to.frame('ifArticleList')
    while page_down <= page:
        print u'正在爬取第 -' + str(page_down) + u'- 页'
        # 翻页
        driver.find_element_by_css_selector(
            '#ajaxElement_2 > table > tbody > tr > td > select > option:nth-child(' + str(page_down) + ')').click()
        driver.implicitly_wait(5)
        for i in range(1, URLnumber + 1):
           # 逐条获取页面URL
            try:
               url_get = driver.find_element_by_css_selector('#ajaxElement_2 > ul > li:nth-child(%d) > a' % i).get_attribute('href')
            except Exception,e:
                print e
                if 'no such element' in str(e):
                    break
                else:
                    pass
            try:
                # 获取信息并导入数据库
                title,ctime,content = information_get(url_get)
                database_connect(title,ctime,content)
            except:
                pass
        page_down = page_down + 1 #页数加1


# 获取标题、时间、内容
def information_get(url):
    # 连接页面并提取相应内容
    html_content = BeautifulSoup(requests.get(url).text.encode('latin1'),'lxml')
    title = html_content.find('h1').text # 标题
    ctime = re.compile(r'(\d{4}-\d{2}-\d{2})').search(html_content.find('div',{'class':'right_content_author'}).text).group() # 时间
    content = ''.join(html_content.find('div',{'class':'right_content_main'}).text.split()) # 内容
    return title,ctime,content

# 连接数据库并导入数据
def database_connect(title,ctime,content):
    conn = mysql.connector.connect(
        host = 'host',
        user = '******',# 用户名
        password = '******',# 密码
        database = '******'# 数据库名称
    )
    cursor = conn.cursor()
    # 尝试导入数据，如数据已经存在则跳过
    cursor.execute('insert into 广西_南宁_青秀_政府办_test'
                   '(title,time,content) values (%s,%s,%s)',[title,ctime,content])
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url = 'http://www.qingxiu.gov.cn/utils/search.html?word=&channelID=13672#Channel_more'
    url_get(1,3,60,url) # 参数依次为起始页数、总页数、每个页面内URL数量、起始页的URL
