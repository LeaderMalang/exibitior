# -*- coding: utf-8 -*-
import scrapy


class ExibitorsipderSpider(scrapy.Spider):
    name = 'exibitorsipder'
    allowed_domains = ['kith.com']
    start_urls = ['https://kith.com']

    def parse(self, response):
        menuItems = response.css('.link--desktop')
        baseUrl = 'https://kith.com'
        for item in menuItems:
            innerContainer = item.css('.site-header__footwear-dropdown-container')
            if innerContainer:
                for inneritem in innerContainer.css('.site-header__footwear-dropdown>li'):
                    # print(inneritem)
                    reqUrl=inneritem.css('a::attr(href)').extract_first()

                    # print('request URL',reqUrl)
                    yield scrapy.Request(url=baseUrl+reqUrl, callback=self.single_parse)
            else:
                reqUrl=item.css('a::attr(href)').extract_first()
                reqPageName=item.css('a::text').extract_first()
                if reqPageName=='News' or reqPageName=='Content':
                    print("not request page")
                else:
                    yield  scrapy.Request(url=baseUrl+reqUrl,callback=self.single_parse)


    def single_parse(self,response):
        print(response)
