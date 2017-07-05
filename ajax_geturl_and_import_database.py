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

# 使用无头浏览器获取URL
def url_get(page_down,page,URLnumber,url):
    url_get_list = []
    # 启动无头浏览器
    driver = webdriver.Chrome(executable_path='E:/chromedriver.exe') # 浏览器名称和路径
    driver.get(url)
    # 路径搜索不到时需要定位frame
    # driver.switch_to.frame('ifArticleList')
    while page_down <= page:
        print u'正在爬取第 -' + str(page_down) + u'- 页'
        driver.implicitly_wait(5)
        # 出错后重新获取该页内容
        try:
            for i in range(1, URLnumber + 1):
                # 逐条获取页面URL
                url_get = driver.find_element_by_css_selector('#ajaxElement_2 > ul > li:nth-child(%d) > a' % i).get_attribute('href')
                # 简单的查重，只限于当次任务
                if url_get[-12:] not in url_get_list:
                    url_get_list.append(url_get[-12:])
                    time.sleep(0.5)
                    # 获取信息并导入数据库
                    title,ctime,content = information_get(url_get)
                    database_connect(title,ctime,content)
            page_down = page_down + 1 #页数加1
        except:
            pass
        # 翻页
        driver.find_element_by_css_selector(
            '#ajaxElement_2 > table > tbody > tr > td > select > option:nth-child(' + str(page_down) + ')').click()

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
        host = 'localhost',
        user = 'root',# 用户名
        password = 'root',# 密码
        database = 'article_url'# 数据库名称
    )
    cursor = conn.cursor()
    # 尝试导入数据，如数据已经存在则跳过
    try:
        cursor.execute('insert into 广西_南宁_青秀_政府办_政务动态'
                   '(title,time,content) values (%s,%s,%s)',[title,ctime,content])
    except:
        pass
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url = 'http://www.qingxiu.gov.cn/utils/search.html?word=&channelID=13125#Channel_more'
    url_get(1,67,60,url) # 参数以此为起始页数、总页数、每个页面内URL数量、起始页的URL