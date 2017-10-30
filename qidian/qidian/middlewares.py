# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from qidian.settings import COMMENTS_URL


class HiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def __init__(self,agentlist):
        self.agentlist = agentlist

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings.getlist('USER_AGENTS'))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            print('process Requests')
            r.headers.setdefault('User-Agent',random.choice(self.agentlist))
            #r.meta["proxy"]='http://117.78.37.198:80'
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)




class AjaxMiddleware(object):
    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            spider.logger.warning('AjaxMiddleware')
            if COMMENTS_URL in r:
                r.headers.update({'Accept':'application/json, text/javascript, */*; q=0.01',
                            'X-Requested-With':'XMLHttpRequest'})

            yield r

    def process_spider_exception(repsonse, exception, spider):
        spider.logger.warning("Something goes wrong!!:",exception)