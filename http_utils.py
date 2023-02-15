"""
http utils
"""
''' --------------------------------------------------------------------------------------- '''

import requests
import json
import traceback

''' --------------------------------------------------------------------------------------- '''
def http_request_header():
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate, br'
    }


''' retire at some point in future as class is better '''
def http_get(url, website='nse'):
    assert website == 'nse', f'{website}: Invalid website'
    base_urls = {'nse': 'https://www.nseindia.com'}

    outcome, tries, err_list = False, 0, []
    while not outcome and tries < 5:
        try:
            session = requests.Session()
            request = session.get(base_urls[website], headers=http_request_header(), timeout=5)
            cookies = dict(request.cookies)
            response = session.get(url, headers=http_request_header(), timeout=5, cookies=cookies)
            if response.status_code == 200:
                result_dict = json.loads(response.text)
                session.close()
                return result_dict
            tries += 1
            err_list.append('ERROR! http_get: code = %d, link = [%s]' % (response.status_code, url))
        except Exception as e:
            tries += 1
            err_list.append('ERROR! Exception: [%s] [%s]' % (e, traceback.format_exc()))
    print('Exhausted retries, http_get failed. Error list\n', err_list)
    return None

class HttpDownloads:
    def __init__(self, website='nse', max_tries=5, timeout=5):
        self.base_urls = {'nse': 'https://www.nseindia.com',
                 'te': 'https://tradingeconomics.com'}
        self.website = website
        self.max_tries = max_tries
        self.timeout  = timeout
        self.counter  = 0
        self.session = None
        self.cookies = None
        self.initialize_session()

    def http_get(self, url):
        if self.counter >= 50:
            self.initialize_session()

        outcome, tries, err_list = False, 0, []
        while not outcome and tries < self.max_tries:
            try:
                response = self.session.get(url, headers=http_request_header(),
                                            timeout=self.timeout, cookies=self.cookies)
                if response.status_code == 200:
                    self.counter += 1
                    return response.text

                err_list.append('HttpDownloads.http_get: code = %d, link = [%s]' %
                                (response.status_code, url))
            except Exception as e:
                err_list.append('HttpDownloads.http_get: [%s] [%s]' % (e, traceback.format_exc()))
            tries += 1
        self.initialize_session()
        raise ValueError('%s: Exhausted retries, http_get failed. err_list::\n%s' % (url, err_list))

    def http_get_json(self, url):
        data = self.http_get(url)
        if data is None or len(data) == 0:
            raise ValueError('http_get failed, data =', data)
        return json.loads(data)

    def http_get_both(self, url):
        data = self.http_get(url)
        if data is None or len(data) == 0:
            raise ValueError('http_get failed, data =', data)
        return json.loads(data), data

    def initialize_session(self):
        if self.session is not None:
            self.session.close()
        self.counter = 0
        self.session = requests.Session()
        request = self.session.get(self.base_urls[self.website], headers=http_request_header(),
                                   timeout=self.timeout)
        self.cookies = dict(request.cookies)