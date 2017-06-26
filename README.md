# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem

class DmozSpider(scrapy.spiders.Spider):
    name = 'dmoz'
    allowed_domains = ['chongzuo.gov.cn']
    start_urls = ['http://www.chongzuo.gov.cn/xwzx/czyw/']

    def parse(self,response):
        for i in range(1,21):
            item = TutorialItem()
            item['title'] = response.xpath('//ul/li[%s]/a[@target="_blank"]/text()'%i).extract()
            print item['title'][0]
