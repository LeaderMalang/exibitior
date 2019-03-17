# -*- coding: utf-8 -*-
import scrapy


class ExibitorsipderSpider(scrapy.Spider):
    name = 'exibitorsipder'
    allowed_domains = ['kith.com']
    start_urls = ['https://http://kith.com']

    def parse(self, response):
        menuItems = response.css('.link--desktop')
        for item in menuItems:
            innerContainer = item.css('.site-header__footwear-dropdown-container')
            if innerContainer:
                for inneritem in innerContainer.css('.site-header__footwear-dropdown>li'):
                    print(inneritem)
                    reqUrl=inneritem.css('a::attr(href)').extract_first()
                detailPage = innerContainer.css('.site-header__footwear-dropdown>li>a::attr(href)').extract_first()
                print(detailPage)
                yield scrapy.Request(url=detailPage, callback=self.single_parse)

    def single_parse(self,response):
        companyName=response.css('h1#hiTitle>span::text').extract_first()
        companyWebsite=response.css('#ContentPlaceHolder1_litURL>a::attr(href)').extract_first()
        stand=response.css('#ContentPlaceHolder1_litStandNo>span::text').extract_first()
        hall=response.css('#ContentPlaceHolder1_litHallNo>span::text').extract_first()
        standManager=response.css('#ContentPlaceHolder1_litStandManager>span::text').extract_first()
        countrylist=response.css('.country-list').xpath('following-sibling::ul[1]/li//text()').extract()

        print(companyName,companyWebsite,stand,hall,countrylist,standManager)
