# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import mysql.connector
import time
import requests
import re
import random

def jobs_info(start_url,page_on,page):
    j = 1
    driver = webdriver.Chrome(executable_path='E:/chromedriver.exe')  # 浏览器名称和路径
    driver.get(start_url)
    #driver.find_element_by_css_selector('#filterCollapse > div:nth-child(1) > div.choose-detail > li > div.other-hot-city > div > a:nth-child(5)').click()
    while page_on <= page:
        print u'正在爬取第 -' + str(page_on) + u'- 页'
        driver.implicitly_wait(5)
        for i in range(1, 16):
            try:
                job_url = driver.find_element_by_css_selector(
                    '#s_position_list > ul > li:nth-child(%d) > div.list_item_top > div.position > div.p_top > a' % i).get_attribute(
                    'href')
            except:
                break
            try:
                print j
                company, name, salary, city, experience, education, work_time, labels, job_advantage, position_description, work_adress = job_details(
                            job_url)
                database_connect(company, name, salary, city, experience, education, work_time, labels, job_advantage,
                                         position_description, work_adress)
                j = j + 1
            except:
                pass
        try:
            driver.find_element_by_css_selector(
                '#order > li > div.item.page > div.next_disabled.next').click()
        except:
            print u'翻页错误'
            break
        page_on = page_on + 1

def job_details(job_url):
    time.sleep(random.randint(1, 3))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3080.5 Safari/537.36',
               'Cookie':'user_trace_token=20170711110036-6244e43c-f79e-4f77-a6b0-1c8f628fa2cd; LGUID=20170711110037-1db7e811-65e5-11e7-a758-5254005c3644; index_location_city=%E6%9D%AD%E5%B7%9E; JSESSIONID=ABAAABAABEEAAJA9F94A93FF8676025156D6356BF18D434; TG-TRACK-CODE=index_navigation; SEARCH_ID=50b8648712d64363bad3c3c5cdcd7995; _gat=1; _gid=GA1.2.862100408.1499913974; _ga=GA1.2.416685032.1499741964; LGSID=20170713104728-9c29b69b-6775-11e7-b69c-525400f775ce; LGRID=20170713111929-150faf24-677a-11e7-b6c5-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499741964,1499906846,1499907009; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1499915895'}
    html_content = BeautifulSoup(requests.get(job_url, headers=headers).text, 'lxml')
    print job_url
    company = html_content.find('div', {'class': 'company'}).text
    name = html_content.find('span', {'class': 'name'}).text
    salary = re.sub(r'[\s|/]', '', html_content.find('span', {'class': 'salary'}).text)
    city = re.sub(r'[\s|/]', '', html_content.find('dd', {'class': 'job_request'}).findAll('span')[1].text)
    experience = re.sub(r'[\s|/]', '', html_content.find('dd', {'class': 'job_request'}).findAll('span')[2].text)
    education = re.sub(r'[\s|/]', '', html_content.find('dd', {'class': 'job_request'}).findAll('span')[3].text)
    work_time = re.sub(r'[\s|/]', '', html_content.find('dd', {'class': 'job_request'}).findAll('span')[4].text)
    try:
        labels = re.sub(r'[\s|/]', '', html_content.find('li', {'class': 'labels'}).text)
    except:
        labels = ''
    job_advantage = re.sub(r'[\s|/| ]', '/', html_content.find('dd', {'class': 'job-advantage'}).find('p').text)
    position_description = re.sub(ur'职位描述：', '', html_content.find('dd', {'class': 'job_bt'}).text)
    work_adress = re.findall(ur'工作地址(.*)查看地图',re.sub(r'[\s|/| ]', '', html_content.find('dd', {'class': 'job-address clearfix'}).text))[0]
    return company,name,salary,city,experience,education,work_time,labels,job_advantage,position_description,work_adress

def database_connect(company,name,salary,city,experience,education,work_time,labels,job_advantage,position_description,work_adress):
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'luffy',# 用户名
        password = '123456',# 密码
        database = 'movie'# 数据库名称
    )
    cursor = conn.cursor()
    # 尝试导入数据，如数据已经存在则跳过
    cursor.execute('insert into lagou_jobs_python数据'
                   '(公司,职位,薪资,城市,经验,学历,全兼职,标签,职位诱惑,职位描述,工作地址) values'
                   '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                   [company,name,salary,city,experience,education,work_time,labels,job_advantage,position_description,work_adress])
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    start_url = 'https://www.lagou.com/jobs/list_python%E6%95%B0%E6%8D%AE?oquery=python%E7%88%AC%E8%99%AB&fromSearch=true&labelWords=relative&city=%E6%9D%AD%E5%B7%9E'
    jobs_info(start_url,page_on=1,page=17)