# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import item


class ExibitorsipderSpider(scrapy.Spider):
    name = 'exibitorsipder'
    allowed_domains = ['kith.com']
    start_urls = ['https://kith.com']
    baseUrl = 'https://kith.com'

    def parse(self, response):
        menuItems = response.css('.link--desktop')

        for item in menuItems:
            innerContainer = item.css('.site-header__footwear-dropdown-container')
            if innerContainer:
                for inneritem in innerContainer.css('.site-header__footwear-dropdown>li'):
                    # print(inneritem)
                    reqUrl=inneritem.css('a::attr(href)').extract_first()

                    # print('request URL',reqUrl)
                    yield scrapy.Request(url=self.baseUrl+reqUrl, callback=self.single_parse)
            else:
                reqUrl=item.css('a::attr(href)').extract_first()
                reqPageName=item.css('a::text').extract_first()
                if reqPageName=='News' or reqPageName=='Content':
                    print("not request page")
                else:
                    yield scrapy.Request(url=self.baseUrl+reqUrl,callback=self.single_parse)


    def single_parse(self,response):

        for items in response.css('.landing-nav__nav>ul>li'):
            reqUrl=items.css('.landing-nav__link::attr(href)').extract_first()
            print(reqUrl)
            if reqUrl:
                yield scrapy.Request(url=self.baseUrl+reqUrl,callback=self.single_category_parse)


    def single_category_parse(self,response):

        print(response)
        products=response.css('ul.collection-products>li.collection-product')
        for product in products:
            reqUrlSingle=product.css('.product-card__image-carousel>a::attr(href)').extract_first()
            print(reqUrlSingle)

            if reqUrlSingle:
                singleProductUrl=self.baseUrl+reqUrlSingle+'.js'
                yield scrapy.Request(url=singleProductUrl,callback=self.single_product_parse)
            else:
                print("No Product found")

    def single_product_parse(self,response):
        print(response.text)
        j = json.loads(response.body_as_unicode())
        items = dict()
        items= {"product":j}
        yield items