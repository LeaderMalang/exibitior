# -*- coding: utf-8 -*-
import scrapy


class ExibitorsipderSpider(scrapy.Spider):
    name = 'exibitorsipder'
    allowed_domains = ['beautyworldme.com']
    start_urls = [
        'https://www.beautyworldme.com/exhibitor-list.aspx?doc_id=565&mkey=&mfl=&msl=&mtl=&mll=&mctry=&mbrd=&mloc=&mst=']

    def parse(self, response):
        containers = response.css('.adv-search-list')
        for container in containers:
            innerContainer = container.css('.adv-search-inner')
            detailPage = innerContainer.css('h2>a::attr(href)').extract_first()
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
