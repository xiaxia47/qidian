# -*- coding=utf-8
import requests


class ProxyFactory(object):
    dblist = ("httpbin", 'free_ipproxy')
    server = "http://13.59.31.164:8000/"
    drop_parms = {'ip': None, 'name': 'httpbin'}

    def __init__(self): 
        self.proxy_list = []
        self.parms = {'sid': 0, 'limit': None}
        self.get_proxies()
        self.limit = 50

    def get_proxy(self, proxy_format=None):
        if len(self.proxy_list) == 0:
            self.limit = limit
            self.get_proxies()
        proxy_in = self.proxy_list.pop()
        proxy_out = None
        if proxy_in['https'] in ['0', 'Fals']:
            proxy_out= {'http':''.join(['http://', proxy_in['ip'],':', str(proxy_in['port'])])}
        else:
            proxy_out= {'https':''.join(['https://', proxy_in['ip'], ':', str(proxy_in['port'])])}
        if proxy_format == 'aiohttp':
            proxy_out = proxy_out['http'] if proxy_in['https'] in ['0', 'Fals'] else proxy_out['https']
            proxy_out = proxy_out.replace('https', 'http')
        return [proxy_out, proxy_in['ip']]

    def get_proxies(self):
        proxy_server = ProxyFactory.server + 'query'
        resp = requests.get(url=proxy_server, params=self.parms)
        self.proxy_list = resp.json()
        if len(self.proxy_list) == 0:
            self.parms['sid'] = 0 
        else:
            self.parms['sid'] = self.proxy_list[-1]['id']

    def drop_proxy(ip_addr,ip):
        proxy_server = ProxyFactory.server + 'delete'
        ip_addr['ip'] = ip
        for database in ProxyFactory.dblist:
            ip_addr['name'] = database
            resp = requests.get(url=proxy_server,params=ip_addr)
            if resp.status_code == 200:
                print('{ip} has been dropped in httpbin and free_proxy'.format(ip=ip))
            else:
                print('Commend failed')

