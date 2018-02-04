# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import UserAgent
from twisted.enterprise import adbapi
import logging
from datetime import datetime,timedelta
from scrapy.exceptions import NotSupported
import pymysql

class RandomUserAgentMiddleware(object):
    '''
    随机更换User-Agent
    '''
    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)


class ProxyMiddleware(object):

    def __init__(self,dbparm):
        self.dbparm = dbparm
        self.proxy_pool = []
        self.drop_list = []
        self.current_proxy = None
        self.proxy_enabled = True


    def getProxyPool(self,drop_list):
        with pymysql.connect(**self.dbparm) as cursor:
            if len(drop_list) > 0:
                format_str=','.join(['%s']* len(drop_list))
                sql = 'update python.proxytable set valid = 1 where address in({})'.format(format_str)
                cursor.execute(sql,tuple(drop_list))
            row_count = cursor.execute('select address from python.proxytable' 
                           ' where valid = 0 order by rank,update_time desc limit 10')
            if row_count >0:
                result = [item[0] for item in cursor.fetchall()]
                return result
            else:
                self.proxy_enabled = False
                raise NotSupported('proxy resources are exhausted')

    
    def renewProxy(self):
        if len(self.proxy_pool) == 0:
            self.proxy_pool = self.getProxyPool(self.drop_list)
            self.drop_list = []
        proxy = self.proxy_pool.pop()
        if proxy not in self.drop_list:
            self.drop_list.append(proxy)
        return proxy


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.getdict("MYSQL_CONFIG"))


    def process_request(self, request, spider):
        if self.proxy_enabled == True:
            if self.current_proxy == None:
                self.current_proxy = self.renewProxy()
            print('proxy is {}'.format(self.current_proxy))
            request.meta['proxy'] = self.current_proxy
            request.meta['dont_redirect'] = True

    def process_exception(self,request, exception, spider):
        if isinstance(exception,NotSupported):
            logging.warning('no Proxy is available now!!!')
        print(exception,type(exception))
        self.current_proxy = None
        return None


    def process_response(self,request, response, spider):
        if 'proxy' in request.meta.keys():
            logging.warning('proxy in use is: {},current response status is {}'.format(
                        request.meta['proxy'], response.status))
        
        print(self.proxy_enabled,response.status)
        if response.status != 200 and self.proxy_enabled == True:
            logging.warning('Abnormal RESP Code:{}! Starting renew-process,current proxy:{} will be dropped'.format(
                            response.status,request.meta['proxy']))
            self.current_proxy = None
            new_request = request.copy()
            return new_request

        return response

