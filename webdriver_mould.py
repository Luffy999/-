# -*- coding:utf-8 -*-

"""
  创建时间：2017-6-23

  作者：Luffy
"""

from selenium import webdriver
import time

#创建存放URL的文件
def open_file(txt):
    file = open('E:\Python_government_url\URL' + txt, 'wb')
    return file

#打开无头浏览器
def open_webdriver(url):
    driver = webdriver.Chrome(executable_path='E:/chromedriver.exe')
    driver.get(url)
    ######### 提示资讯链接的路径不存在时，需要重新定位frame
    ######### driver.switch_to.frame('ifArticleList')
    return driver

#爬取资讯链接
def get_pageURL(txt,url,page_on=1):
    file = open_file(txt)
    driver = open_webdriver(url)
    driver.implicitly_wait(5)
    url_get_list = []
    while page_on <= page:
        print u'正在爬取第 -'+str(page_on)+u'- 页'
        time.sleep(1)
        try:
            for i in range(1,number+1):
                #########对页面内资讯的URL迭代抓取
                url_get = driver.find_element_by_css_selector(URL_selector %i).get_attribute('href')
                #########查重
                if url_get[-12:] not in url_get_list:
                    url_get_list.append(url_get[-12:])
                    file.write(url_get+'\r\n')
            page_on = page_on+1
            driver.find_element_by_css_selector('#ajaxElement_2 > table > tbody > tr > td > select > option:nth-child('+str(page_on)+')').click()
        except:
            pass
        #########翻页的路径有可能会变化
    print u'\n------结束------'
    file.close()
    driver.quit()

if __name__ == '__main__':
    txt = u'\广西_南宁_青秀_政府办_政务动态.txt'
    url = "http://www.qingxiu.gov.cn/utils/search.html?word=&channelID=10755#Channel_more"
    URL_selector = '#ajaxElement_2 > ul > li:nth-child(%d) > a'
    page = 104
    number = 60
    get_pageURL(txt,url)