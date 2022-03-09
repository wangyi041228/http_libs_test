import asyncio
import http.client
import statistics
import time
import urllib.request

import grequests  # 需在requests和派生库之前
import aiohttp
import httpx
import requests
import urllib3
import json

U = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
H = {
    'User-Agent': U,
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Encoding': 'gzip',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7,en-US;q=0.6',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'authorization': '',
}
HJ = {
    'User-Agent': U,
    'Content-Type': 'application/json',
}
P = 'localhost', 114514
PS = f'{P[0]}:{str(P[1])}'
P0 = 'http://' + PS
P1 = {'http': P0, 'https': P0}
P2 = {'http': P0}


def get_httplib(url, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    _host_param = url.split('//', 1)[1]
    _pos = _host_param.find('/')
    if _pos > 0:
        _host, _param = _host_param[:_pos], _host_param[_pos:]
    else:
        _host, _param = _host_param, '/'
    if withproxy:
        _conn = http.client.HTTPSConnection(P[0], P[1])
        _conn.set_tunnel(_host)
        _conn.request('GET', _param, headers=headers)
        _res = _conn.getresponse()
        _len = len(_res.read())
        _status = _res.status
        _conn.close()
    else:
        _conn = http.client.HTTPSConnection(_host)
        _conn.request('GET', _param, headers=headers)
        _res = _conn.getresponse()
        _len = len(_res.read())
        _status = _res.status
        _conn.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def post_httplib(url, data=None, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    _host_param = url.split('//', 1)[1]
    _pos = _host_param.find('/')
    if _pos > 0:
        _host, _param = _host_param[:_pos], _host_param[_pos:]
    else:
        _host, _param = _host_param, '/'
    if withproxy:
        _conn = http.client.HTTPSConnection(P[0], P[1])
        _conn.set_tunnel(_host)
        _conn.request('POST', _param, json.dumps(data), headers=headers)
        _res = _conn.getresponse()
        _len = len(_res.read())
        _status = _res.status
        _conn.close()
    else:
        _conn = http.client.HTTPSConnection(_host)
        _conn.request('POST', _param, json.dumps(data), headers=headers)
        _res = _conn.getresponse()
        _len = len(_res.read())
        _status = _res.status
        _conn.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def get_urllib(url, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()

    # with urllib.request.urlopen(url) as res:

    rrr = urllib.request.Request(url, headers=headers)
    if withproxy:
        rrr.set_proxy(PS, 'http')
    with urllib.request.urlopen(rrr) as res:

        _len = len(res.read())
        _status = res.status
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def post_urllib(url, data=None, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()

    # with urllib.request.urlopen(url) as res:

    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers, method='POST')
    if withproxy:
        req.set_proxy(PS, 'http')
    with urllib.request.urlopen(req) as res:

        _len = len(res.read())
        _status = res.status
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def get_urllib3(url, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    if withproxy:
        pm = urllib3.ProxyManager(P0)
    else:
        pm = urllib3.PoolManager()
    res = pm.request('GET', url, headers=headers)
    _len = len(res.data)
    _status = res.status
    res.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def post_urllib3(url, data=None, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    if withproxy:
        pm = urllib3.ProxyManager(P0)
    else:
        pm = urllib3.PoolManager()
    res = pm.request('POST', url, body=json.dumps(data), headers=headers)
    _len = len(res.data)
    _status = res.status
    res.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def get_requests(url, headers=None, withproxy=False):
    if withproxy:
        proxies = P1
    else:
        proxies = None
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    res = requests.get(url, proxies=proxies, headers=headers)  # verify=False
    _len = len(res.content)
    _status = res.status_code
    res.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def post_requests(url, data=None, headers=None, withproxy=False):
    if withproxy:
        proxies = P1
    else:
        proxies = None
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    res = requests.post(url, json=data, proxies=proxies, headers=headers)
    _len = len(res.content)
    _status = res.status_code
    res.close()
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


async def get_aiohttp_basic(url, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    if withproxy:
        proxy = P0
    else:
        proxy = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, proxy=proxy) as res:
            _text = await res.read()
            _status = res.status
            return _status, _text


async def post_aiohttp_basic(url, data=None, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    if withproxy:
        proxy = P0
    else:
        proxy = None
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers, proxy=proxy) as res:
            _text = await res.read()
            _status = res.status
            return _status, _text


def get_aiohttp(url, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    tasks = [get_aiohttp_basic(url, headers=headers, withproxy=withproxy)]
    result = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))[0]
    _dt = time.perf_counter() - _start
    return result[0], _dt, len(result[1]), result[1]


def gets_aiohttp(urls, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    tasks = [get_aiohttp_basic(url, headers=headers, withproxy=withproxy) for url in urls]
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    _dt = time.perf_counter() - _start
    return results, _dt


def post_aiohttp(url, data=None, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    tasks = [post_aiohttp_basic(url, data=data, headers=headers, withproxy=withproxy)]
    result = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))[0]
    _dt = time.perf_counter() - _start
    return result[0], _dt, len(result[1]), result[1]


def posts_aiohttp(url_data_list, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    tasks = [post_aiohttp_basic(ud[0], data=ud[1], headers=headers, withproxy=withproxy) for ud in url_data_list]
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    _dt = time.perf_counter() - _start
    return results, _dt


def get_httpx(url, headers=None, withproxy=False):
    if withproxy:
        proxies = P0
    else:
        proxies = None
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    res = httpx.get(url, proxies=proxies, headers=headers)
    _len = len(res.read())
    _status = res.status_code
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def post_httpx(url, data=None, headers=None, withproxy=False):
    if withproxy:
        proxies = P0
    else:
        proxies = None
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    res = httpx.post(url, json=data, proxies=proxies, headers=headers)
    _len = len(res.read())
    _status = res.status_code
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def get_grequests(url, headers=None, withproxy=False):
    def exception_handler(request, exception):
        print(exception)
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    if withproxy:
        proxies = P2
        req = (grequests.get(url, verify=False, proxies=proxies, headers=headers),)
    else:
        proxies = None
        req = (grequests.get(url, proxies=proxies, headers=headers),)
    res_all = grequests.map(req, exception_handler=exception_handler)
    res = res_all[0]
    _len = len(res.content)
    _status = res.status_code
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def gets_grequests(urls, headers=None, withproxy=False):
    def exception_handler(request, exception):
        print(exception)
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    if withproxy:
        proxies = P2
        req = (grequests.get(url, verify=False, proxies=proxies, headers=headers) for url in urls)
    else:
        proxies = None
        req = (grequests.get(url, proxies=proxies, headers=headers) for url in urls)
    res_all = grequests.map(req, exception_handler=exception_handler)
    results = [(res.status_code, res.content) if res else (0, '') for res in res_all]
    _dt = time.perf_counter() - _start
    return results, _dt


def post_grequests(url, data=None, headers=None, withproxy=False):
    if withproxy:
        proxies = P1
    else:
        proxies = None
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    req = (grequests.post(url, json=data, proxies=proxies, headers=headers),)
    res = grequests.map(req)[0]
    _len = len(res.content)
    _status = res.status_code
    _dt = time.perf_counter() - _start
    return _status, _dt, _len


def posts_grequests(url_data_list, headers=None, withproxy=False):
    def exception_handler(request, exception):
        print(exception)
    if headers is None:
        headers = {}
    _start = time.perf_counter()
    if withproxy:
        proxies = P2
        req = (grequests.post(ud[0], json=ud[1], proxies=proxies, headers=headers) for ud in url_data_list)
    else:
        proxies = None
        req = (grequests.post(ud[0], json=ud[1], proxies=proxies, headers=headers) for ud in url_data_list)
    res_all = grequests.map(req, exception_handler=exception_handler)
    results = [(res.status_code, res.content) if res else (0, '') for res in res_all]
    _dt = time.perf_counter() - _start
    return results, _dt


def results_handler(func_name, results):
    status_list = [result[0] for result in results]
    dt_list = [result[1] for result in results]
    len_list = [result[2] for result in results]
    count_succuss = status_list.count(200)
    count_fail = len(results) - count_succuss
    dt_mean = statistics.mean(dt_list)
    dt_stdev = statistics.stdev(dt_list) if len(results) > 1 else 0.0
    len_mean = statistics.mean(len_list)
    len_stdev = statistics.stdev(len_list) if len(results) > 1 else 0.0
    print("{:<15}{:>10.3f} ±{:<10.3f}{:>15.1f} ±{:<10.1f}{:>10} /{}".format(
        func_name, dt_mean, dt_stdev, len_mean, len_stdev, count_succuss, count_fail))


def results_handler2(func_name, results):
    status_list = [result[0] for result in results[0]]
    len_list = [len(result[1]) for result in results[0]]
    dt = results[1]
    count_succuss = status_list.count(200)
    count_fail = len(status_list) - count_succuss
    len_mean = statistics.mean(len_list)
    len_stdev = statistics.stdev(len_list) if len(len_list) > 1 else 0.0
    print("{:<15}{:>15.3f}     {:>15.1f} ±{:<10.1f}{:>10} /{}".format(
        func_name, dt, len_mean, len_stdev, count_succuss, count_fail))


def compare_sync(method, url, data=None, times=1, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    print(f'{times}次顺序{method}测试')
    print('URL:', url)
    print("{:^15}{:>10} ±{:<10}{:>15} ±{:<10}{:>10} /{}".format(
        'lib', 'mean time', 'stdev(s)', 'mean bytes', 'stdev', '200', 'e'))
    if method == 'GET':
        function_list = [
            get_httplib,
            get_urllib,
            get_urllib3,
            get_requests,
            get_aiohttp,
            get_httpx,
            get_grequests,
        ]
        for func in function_list:
            func_results = [func(url, headers=headers, withproxy=withproxy) for _ in range(times)]
            results_handler(func.__name__, func_results)
    elif method == 'POST':
        function_list = [
            post_httplib,
            post_urllib,
            post_urllib3,
            post_requests,
            post_aiohttp,
            post_httpx,
            post_grequests,
        ]
        for func in function_list:
            func_results = [func(url, data=data, headers=headers, withproxy=withproxy) for _ in range(times)]
            results_handler(func.__name__, func_results)
    else:
        return
    print()


def compare_async(method, url_data, times=10, headers=None, withproxy=False):
    if headers is None:
        headers = {}
    print(f'{times}次独立会话异步{method}测试')
    print('URL/data:', url_data)
    print("{:^15}{:>10}{:<10}{:>15} ±{:<10}{:>10} /{}".format(
        'lib', 'total ', 'time(s)', 'mean bytes', 'stdev', '200', 'e'))
    if method == 'GET':
        function_list = [
            gets_aiohttp,
            gets_grequests,
        ]
        for func in function_list:
            func_results = func([url_data] * times, headers=headers, withproxy=withproxy)
            results_handler2(func.__name__, func_results)
    elif method == 'POST':
        function_list = [
            posts_aiohttp,
            posts_grequests,
        ]
        for func in function_list:
            func_results = func([url_data] * times, headers=headers, withproxy=withproxy)
            results_handler2(func.__name__, func_results)
    else:
        return
    print()


if __name__ == '__main__':
    url_baidu = 'https://www.baidu.com'
    url_bin_get = 'https://httpbin.org/get'
    url_bin_post = 'https://httpbin.org/post'
    url_rito = 'https://developer.riotgames.com/docs/lor'
    url_zip = 'https://dd.b.pvp.net/latest/set2-en_us.zip'
    url_img = 'https://dd.b.pvp.net/latest/set5/en_us/img/cards/05BC001.png'
    url_json = 'https://dd.b.pvp.net/latest/set5/en_us/data/set5-en_us.json'
    url_game = 'https://play.skyweaver.net/account/0x40e73bc20d98dfe28e4d793a9fd542d8d6b18b61'

    for test_url in [
        url_baidu,
        url_bin_get,
        # url_rito,
        # url_zip,
        url_img,
        # url_json,
        # url_game,
    ]:
        compare_sync('GET', test_url, times=5, headers=H, withproxy=False)

    for test_url, post_data in [
        # ('https://metadata.sequence.app/rpc/Metadata/GetNiftyswapTokenQuantity',
        #  {"chainID": "137", "contractAddress": "0x9B609Bf3A3977Ee7254210E0A0D835251540c4D5", "tokenIDs": ['131073']}),
        (url_bin_post, {'a': 'A'}),
    ]:
        compare_sync('POST', test_url, data=post_data, times=5, headers=HJ, withproxy=False)

    for test_url in [
        url_baidu,
        url_bin_get,
        # url_rito,
        # url_zip,
        url_img,
        # url_json,
        # url_game,
    ]:
        compare_async('GET', test_url, times=100, headers=H, withproxy=False)

    for test_url_data in [
        (url_bin_post, {'a': 'A'}),
    ]:
        compare_async('POST', test_url_data, times=100, headers=HJ, withproxy=False)
