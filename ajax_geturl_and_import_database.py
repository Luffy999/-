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
    # 启动无头浏览器
    driver = webdriver.Chrome(executable_path='******') # 浏览器名称和路径
    driver.get(url)
    #driver.find_element_by_css_selector('#pageNum > span:nth-child(2)').click()
    driver.implicitly_wait(5)
    # 路径搜索不到时需要定位frame
    #driver.switch_to.frame('ifArticleList')
    while page_down <= page:
        print u'正在爬取第 -' + str(page_down) + u'- 页'
        driver.implicitly_wait(5)
        for i in range(1, URLnumber + 1):
           # 逐条获取页面URL
            try:
                url_gets = driver.find_element_by_css_selector(
                    '#middle02_r > div.list02 > ul > li:nth-child(' + str(i * 2) + ') > a').get_attribute('href')
                time.sleep(0.5)
                print url_gets
                # 获取信息并导入数据库
                title,ctime,content = information_get(url_gets)
                database_connect(title,ctime,content)
            except Exception,e:
                pass
        # 翻页
        #driver.implicitly_wait(5)
        try:
            page_down = page_down + 1  # 页数加1
            driver.find_element_by_css_selector('#ctl00\\24 ContentPlaceHolder_middle\\24 AspNetPager1_input > option:nth-child(' + str(page_down) + ')').click()
            #if page_down == 2:
                #driver.find_element_by_css_selector('#fanye > table > tbody > tr > td:nth-child(1) > a:nth-child(1)').click()
            #else:
                #driver.find_element_by_css_selector('#fanye > table > tbody > tr > td:nth-child(1) > a:nth-child(3)').click()
        except Exception,e:
            print e
            if 'no such element' in str(e):
                break
            else:
                print time.ctime()
                page_down = page_down - 1
                pass

# 获取标题、时间、内容
def information_get(url):
    # 连接页面并提取相应内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36'}
    html_content = BeautifulSoup(requests.get(url, headers=headers).text.encode('latin1'), 'lxml')
    title = re.sub(r'\s','',html_content.find('h3',{'align':'center'}).text) # 标题
    time = re.compile(r'(\d{4}-\d{1,2}-\d{1,2})').search(html_content.find_all('td',{'align':'center'})[2].text).group()  # 时间
    content = re.sub(r'\s','',html_content.find_all('td',{'class':'font'})[1].text) # 内容
    return title,time,content

# 连接数据库并导入数据
def database_connect(title,ctime,content):
    conn = mysql.connector.connect(
        host = 'localhost',# 服务器名称
        user = '******',# 用户名
        password = '******',# 密码
        database = '******'# 数据库名称
    )
    cursor = conn.cursor()
    # 尝试导入数据，如数据已经存在则跳过
    cursor.execute('insert into 广西_防城港_市级_环保局_县区动态'
                   '(title,time,content) values (%s,%s,%s)',[title,ctime,content])
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url = 'http://fcghbj.gov.cn/ChannelMess/List.aspx?Channel_ID=7'
    url_get(1,3,20,url) # 参数以此为起始页数、总页数、每个页面内URL数量、起始页的URL
