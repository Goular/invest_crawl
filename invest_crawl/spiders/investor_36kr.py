# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http.request import Request


class Investor36krSpider(scrapy.Spider):
    name = 'investor_36kr'
    allowed_domains = ['36kr.com']

    # 最大页数，从第一页开始读
    max_page = 0

    # User-Agent
    ua = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0'}
    # 首次抓取的网页
    start_url = "https://rong.36kr.com/n/api/search/user?p={page}"
    # 首次抓取网站的参数
    page = "1"

    def start_requests(self):
        # 获取列表的json返回
        yield Request(self.start_url.format(page=self.page), headers=self.ua, callback=self.parse_investor_list_index)

    # 解析投资人列表内容
    def parse_investor_list_index(self, response):
        raw_results = json.loads(response.text)
        data = raw_results['data']
        pageData = data['pageData']
        # 列表数据
        listDatas = pageData['data']
        # 当前总共多少页
        totalPages = pageData['totalPages']
        # 总数量
        totalCount = pageData['totalCount']
        # 当前的页数列表的数量
        pageSize = pageData['pageSize']
        # 当前页数
        page = pageData['page']
        next_page = 1
        self.current_page = page
        # 判断是否是第一页
        if str(page) == '1' and totalPages > 1:
            # 只有在页数为1的时候才会触发
            self.max_page = totalPages
        # 下一个需要爬取的页数
        if page < self.max_page:
            next_page = page + 1

        # 添加列表的数据解析到Scheduler
        self.parse_investor_list_detail(listDatas)

        # 若next_page存在，那么继续请求下一页数据
        if next_page > page:
            yield Request(self.start_url.format(page=next_page), headers=self.ua,
                          callback=self.parse_investor_list_index)

    def parse_investor_list_detail(self, data):
        for i in range(len(data)):
            # 获取ID，然后构造出新的需要保存的数据
            tmpData = data[i]
            investor_id = tmpData['id']
            print(investor_id)
