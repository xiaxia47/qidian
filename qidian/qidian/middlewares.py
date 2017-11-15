# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent

class RandomUserAgentMiddleware(object):
    '''
    随机更换User-Agent
    '''
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware,self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
