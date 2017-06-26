# -*- coding:utf-8 -*-
# ------------------------------------------------------
#   版本：py2.7
#   日期：2017-06-23
#   作者：Luffy
# ------------------------------------------------------

from bs4 import BeautifulSoup
import requests

# 获取图片链接
def get_urls(url):
    html_doc=requests.get(url)
    html_text=BeautifulSoup(html_doc.text,'lxml')
    img_urls=html_text.find_all('img',class_="imageWrapper")
    return img_urls

# 下载图片
def get_img(url):
    img_urls = get_urls(url)
    for img_url in img_urls:
        # 拼接成高清图片的链接
        img_src='http://www.ikea.com'+img_url['src'][:-19]+img_url['src'][-13:]
        # 保存图片，需要新建名为'picture_1'的文件夹
        with open('picture_1/'+img_url['title']+'.jpg','wb') as f:
            f.write(requests.get(img_src).content)

if __name__ == '__main__':
    url = 'http://www.ikea.com/cn/zh/catalog/categories/departments/bedroom/tools/cobe/roomset/'
    get_img(url)
