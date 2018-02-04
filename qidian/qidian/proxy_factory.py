# -*- coding=utf-8
import requests

class ProxyFactory(object):
    dblist = ['httpbin','free_ipproxy']
    server = 'http://13.59.31.164:8000/'
    drop_parms = {'ip':None,'name':'httpbin'}
    def __init__(self): 
        self.proxy_list = []
        self.parms = {'sid':0,'limit':None}
        self.get_proxies()
        self.limit = 10

    def pop_proxy(self,proxy_format=None):
        for proxy_in in self.proxy_list:
            proxy_out = None
            if proxy_in['https'] in ['0','Fals']:
                proxy_out= {'http':''.join(['http://',proxy_in['ip'],':',str(proxy_in['port'])])}
            else:
                proxy_out= {'https':''.join(['https://',proxy_in['ip'],':',str(proxy_in['port'])])}
            if proxy_format == 'aiohttp':
                proxy_out = proxy_out['http'] if proxy_in['https'] in ['0','Fals'] else proxy_out['https']
                proxy_out = proxy_out.replace('https','http')
            yield [proxy_out,proxy_in['ip']]

   
    def set_limit(self,limit):
        if limit.isNumeric():
           self.limit = int(limit)


    def get_proxy(self):
        try:
            return next(self.pop_proxy())
        except Exception as e:
            self.get_proxies()
        return next(self.pop_proxy())


    def get_proxies(self):
        proxy_server = ProxyFactory.server + 'query'
        resp = requests.get(url=proxy_server,params=self.parms)
        self.proxy_list = resp.json()
        if len(self.proxy_list) == 0:
            self.parms['sid'] = 0 
        else:
            self.parms['sid'] = self.proxy_list[-1]['id']
        

    def drop_proxy(proxy,ip):
        proxy_server = ProxyFactory.server + 'delete'
        drop_parms['ip'] = ip
        for database in ProxyFactory.dblist:
            drop_parms['name'] = database
            resp = requests.get(url=proxy_server,params=drop_parms)
            if resp.status_code == 200:
                print('{ip} has been dropped in httpbin and free_proxy'.format(ip=ip))
            else:
                print('Commend faileda')

