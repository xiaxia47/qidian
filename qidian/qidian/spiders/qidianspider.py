# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from qidian.items import QidianItem
from urllib.parse import urlencode
import copy
import json

class QidianSpider(scrapy.Spider):
    name = 'Qidian'
    allowed_domain=['www.qidian.com',
                    'book.qidian.com']
    

    def start_requests(self):
        urls = 'https://www.qidian.com/all?'
        #for chanid in self.settings.getdict('CHANIDLIST').items():
        #yield scrapy.Request(urls,body=self.get_body(chanid,1),dont_filter=True)
#        print('request start')
#        url = 'https://www.qidian.com/all?chanId=21&orderId=&page=1&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0'
#        yield scrapy.Request(url,dont_filter=True)
        request_body= self.settings.getdict('DEFAULT_PARAM')
#        request_body= self.settings.getdict('DEFAULT_PARAM')
        for chanid in self.settings.getdict('CHANIDLIST').values():
            request_body['chanId']= chanid
            for page in range(1,20):
                request_body['page']=page
                url = 'https://www.qidian.com/all?'+urlencode(request_body)
                yield scrapy.Request(url,dont_filter=True)


    def get_body(self,chanid,page):
        request_body= self.settings.getdict('DEFAULT_PARAM')
        return request_body

    def parse(self,response):
        bot = Selector(response)
        csrfToken = self.get_cookies('_csrfToken',response)
        contents = bot.xpath('//tbody/tr')
        for content in contents:
            item = QidianItem()
            item['book_type'] = content.xpath('td[1]/a[1]/text()').extract_first()
            item['book_sub_type'] = content.xpath('td[1]/a[2]/text()').extract_first()
            item['book_name']= content.xpath('td[2]/a[1]/text()').extract_first()
            item['book_url'] = 'https:' + content.xpath('td[2]/a[1]/@href').extract_first()
            item['total_words'] = content.xpath('td[4]/span/text()').extract_first()
            item['author'] = content.xpath('td[5]/a/text()').extract_first()
            item['last_upload_date'] = content.xpath('td[6]/text()').extract_first()
            yield scrapy.Request(item['book_url'],meta={'item':item,'csrfToken':csrfToken},
                            callback=self.parse_detail)


    def parse_detail(self,response):
        bot = Selector(response)
        item = response.meta['item']
        item['book_status'] = bot.xpath("//div/p/span[@class='blue'][1]/text()").extract_first()
        click_content=bot.xpath('normalize-space(//div[2]/p[3])').extract_first()
        item['click_count'] = click_content.split('|')[1].split('·')[0]
        item['recommand_count'] = click_content.split('|')[2].split('·')[0]
        item['book_id'] = item['book_url'].split('/')[-1]
        detail_params = copy.deepcopy(self.settings.getdict('DEFAULT_COMEMENT_PARM'))
        detail_params['_csrfToken'] = response.meta['csrfToken']
        detail_params['bookId']= item['book_id']
        next_url = self.settings.get('COMMENTS_URL')+urlencode(detail_params)
        yield scrapy.Request(next_url,meta={'item':item},callback=self.parse_rank)


    def get_cookies(self,cookie_key,response):
        cookie_list = response.headers.getlist('Set-Cookie')[0].decode('utf-8').split(';')
        for cookie in cookie_list:
            if cookie_key in cookie:
                return cookie.strip().split('=')[-1]
        self.logger.info('ERORR:Cookie not found!! KEY is {}'.format(cookie_key))
        return ''


    def parse_rank(self,response):
        jsondata = json.loads(response.text)
        item = response.meta['item']
        item['rank_score'] = jsondata['data']['rate']
        item['rank_ppl_involved'] = jsondata['data']['userCount']
        yield item
    