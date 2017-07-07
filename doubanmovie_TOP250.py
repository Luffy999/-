# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
import requests
import re
import random

def movie_info():
    for i in range(0,250,25):
        print u'正在爬取第 -' + str((i+25)/25) + u'- 页'
        url = 'https://movie.douban.com/top250?start=%d&filter='%i
        time.sleep(random.randint(1,3))
        html_content = BeautifulSoup(requests.get(url).text,'lxml')
        movie_urls = re.findall(r'<a class="" href="(https.*)">',str(html_content))
        for movie_url in movie_urls:
            try:
                name, year, director, screenwriter, actor, genre, area, mins, rating_num, rating_poeple, rating_5, rating_4, rating_3, rating_2, rating_1, betterthan = movie_details(movie_url)
                database_connect(name, year, director, screenwriter, actor, genre, area, mins, rating_num, rating_poeple,rating_5, rating_4, rating_3, rating_2, rating_1, betterthan)
            except:
                pass

def movie_details(movie_url):
    time.sleep(random.randint(1, 3))
    html_content = BeautifulSoup(requests.get(movie_url).text,'lxml')
    name = html_content.find('span',property="v:itemreviewed").text
    year = html_content.find('span',{'class':'year'}).text
    director = html_content.find_all('span',{'class':'attrs'})[0].text
    screenwriter = html_content.find_all('span',{'class':'attrs'})[1].text
    actor = html_content.find_all('span',{'class':'attrs'})[2].text
    genre = ''
    for g in html_content.find_all('span',{'property':'v:genre'}):
        genre = genre + g.text
    area = re.findall(r'<span class="pl">制片国家/地区:</span>\s?(.*)<br/>',str(html_content))[0]
    mins = html_content.find('span',{'property':'v:runtime'}).text
    rating_num = html_content.find('strong',{'property':'v:average'}).text
    rating_poeple = html_content.find('span',{'property':'v:votes'}).text
    rating_5 = html_content.find_all('span',{'class':'rating_per'})[0].text
    rating_4 = html_content.find_all('span',{'class':'rating_per'})[1].text
    rating_3 = html_content.find_all('span',{'class':'rating_per'})[2].text
    rating_2 = html_content.find_all('span',{'class':'rating_per'})[3].text
    rating_1 = html_content.find_all('span',{'class':'rating_per'})[4].text
    betterthan = re.sub(r'\s','',html_content.find('div',{'class':'rating_betterthan'}).text)
    return name,year,director,screenwriter,actor,genre,area,mins,rating_num,rating_poeple,rating_5,rating_4,rating_3,rating_2,rating_1,betterthan

def database_connect(name,year,director,screenwriter,actor,genre,area,mins,rating_num,rating_poeple,rating_5,rating_4,rating_3,rating_2,rating_1,betterthan):
    conn = mysql.connector.connect(
        host = 'host',
        user = 'user',# 用户名
        password = 'password',# 密码
        database = 'database'# 数据库名称
    )
    cursor = conn.cursor()
    # 尝试导入数据，如数据已经存在则跳过
    cursor.execute('insert into doubanmovie_TOP250'
                   '(电影名称,年份,导演,编剧,主演,类型,制片国家,片长,评分,评价人数,5星,4星,3星,2星,1星,好于) values'
                   ' (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [name,year,director,screenwriter,actor,genre,area,mins,rating_num,rating_poeple,rating_5,rating_4,rating_3,rating_2,rating_1,betterthan])
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    movie_info()
