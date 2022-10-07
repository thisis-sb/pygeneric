import requests
import json
import traceback

def http_get(url, website='nse'):
    assert website == 'nse', f'{website}: Invalid website'
    base_urls = {'nse':'https://www.nseindia.com'}

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                             '(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
               'accept-language': 'en,gu;q=0.9,hi;q=0.8',
               'accept-encoding': 'gzip, deflate, br'
    }

    outcome, tries, err_list = False, 0, []
    while not outcome and tries < 5:
        try:
            session = requests.Session()
            request = session.get(base_urls[website], headers=headers, timeout=5)
            cookies = dict(request.cookies)
            response = session.get(url, headers=headers, timeout=5, cookies=cookies)
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