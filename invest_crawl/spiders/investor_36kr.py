# -*- coding: utf-8 -*-
import scrapy


class Investor36krSpider(scrapy.Spider):
    name = 'investor_36kr'
    allowed_domains = ['36kr.com']
    start_urls = ['http://36kr.com/']

    def parse(self, response):
        pass
