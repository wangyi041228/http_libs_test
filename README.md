# http_libs_test
汇总常见HTTP客户端库的基础用法，对比性能。
## 测试库
1) [http.client / httplib](https://docs.python.org/zh-cn/3/library/http.client.html)
2) [urllib](https://docs.python.org/zh-cn/3/library/urllib.request.html)
3) [urllib3](https://urllib3.readthedocs.io/en/stable)
4) [requests](https://docs.python-requests.org/en/latest)
5) [aiohttp](https://docs.aiohttp.org)
6) [httpx](https://www.python-httpx.org)
7) [grequests](https://github.com/spyoungtech/grequests)
## 后续库
1) [requests-futures](https://github.com/ross/requests-futures)
2) [requests-threads](https://github.com/requests/requests-threads)
3) [pycurl](http://pycurl.io)
4) [requests_cpp](https://github.com/daimiaopeng/fast_requests) 依赖py3072？
5) [treq](https://github.com/twisted/treq)
6) [httplib2](https://github.com/jcgregorio/httplib2)
7) [Scrappy框架](https://scrapy.org)
8) [selenium框架](https://www.selenium.dev)
9) [MechanicalSoup](https://mechanicalsoup.readthedocs.io/en/stable)
## 测试用例
1) GET [百度](https://www.baidu.com)
2) GET/POST [httpbin](https://httpbin.org)
3) GET [网页](https://developer.riotgames.com/docs/lor)
4) GET [二进制大文件](https://dd.b.pvp.net/latest/set1-en_us.zip)
5) GET [二进制小文件](https://dd.b.pvp.net/latest/set5/en_us/img/cards/05BC001.png)
6) GET [JSON文件](https://dd.b.pvp.net/latest/set5/en_us/data/set5-en_us.json)
7) POST [Skyweaver查询](https://metadata.sequence.app/rpc/Metadata/GetNiftyswapTokenQuantity)
8) GET/POST [requestbin](https://requestbin.com)
## 现有问题
1) 使用`urllib`时，如有代理，访问百度返回结果为`gb2312`字符集，内容少。
2) 使用`requests`时，如有代理，但传`proxies=None`或默认，没设置`verify=False`会各自报错。
3) 使用`grequests`时，如有代理报错，摸索无果。需进一步了解`requests.session`。
## 补充说明
1) 不提倡为每个url开单独的会话，尽量同一主机只开一个会话。
2) 学习行为，请勿上升到攻击。
3) grequests要写句柄输出异常。
## 简易结果
5次顺序GET测试

URL: https://www.baidu.com

| lib | mean time ±stdev(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| get_httplib | 0.151 ±0.063 | 349576.4 ±1540.5 | 5 /0 |
| get_urllib | 0.111 ±0.005 | 348882.8 ±19.5 | 5 /0 |
| get_urllib3 | 0.128 ±0.040 | 349547.8 ±1557.2 | 5 /0 |
| get_requests | 0.074 ±0.013 | 348894.8 ±20.5 | 5 /0 |
| get_aiohttp | 0.073 ±0.008 | 348876.6 ±29.4 | 5 /0 |
| get_httpx | 0.083 ±0.018 | 348872.4 ±27.2 | 5 /0 |
| get_grequests | 0.082 ±0.022 | 348879.4 ±25.5 | 5 /0 |

5次顺序GET测试

URL: https://httpbin.org/get

| lib | mean time ±stdev(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| get_httplib | 1.093 ±0.009 | 370.0 ±0.0 | 5 /0 |
| get_urllib | 1.101 ±0.020 | 370.0 ±0.0 | 5 /0 |
| get_urllib3 | 1.107 ±0.026 | 370.0 ±0.0 | 5 /0 |
| get_requests | 1.084 ±0.017 | 397.0 ±0.0 | 5 /0 |
| get_aiohttp | 1.070 ±0.011 | 397.0 ±0.0 | 5 /0 |
| get_httpx | 1.095 ±0.040 | 397.0 ±0.0 | 5 /0 |
| get_grequests | 1.098 ±0.030 | 397.0 ±0.0 | 5 /0 |

5次顺序GET测试

URL: https://dd.b.pvp.net/latest/set5/en_us/img/cards/05BC001.png

| lib | mean time ±stdev(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| get_httplib | 0.473 ±0.082 | 588110.0 ±0.0 | 5 /0 |
| get_urllib | 0.443 ±0.030 | 588110.0 ±0.0 | 5 /0 |
| get_urllib3 | 0.419 ±0.012 | 588110.0 ±0.0 | 5 /0 |
| get_requests | 0.435 ±0.019 | 588110.0 ±0.0 | 5 /0 |
| get_aiohttp | 0.446 ±0.040 | 588110.0 ±0.0 | 5 /0 |
| get_httpx | 0.460 ±0.023 | 588110.0 ±0.0 | 5 /0 |
| get_grequests | 0.431 ±0.061 | 588110.0 ±0.0 | 5 /0 |

5次顺序POST测试

URL/data: ('https://httpbin.org/post', {'a': 'A'})

| lib | mean time ±stdev(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| post_httplib | 1.092 ±0.009 | 532.0 ±0.0 | 5 /0 |
| post_urllib | 1.231 ±0.161 | 532.0 ±0.0 | 5 /0 |
| post_urllib3 | 1.128 ±0.057 | 532.0 ±0.0 | 5 /0 |
| post_requests | 1.139 ±0.132 | 559.0 ±0.0 | 5 /0 |
| post_aiohttp | 1.090 ±0.015 | 559.0 ±0.0 | 5 /0 |
| post_httpx | 1.415 ±0.025 | 559.0 ±0.0 | 5 /0 |
| post_grequests | 1.118 ±0.034 | 559.0 ±0.0 | 5 /0 |

100次独立会话异步GET测试

URL/data: https://www.baidu.com

| lib | total time(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| gets_aiohttp | 0.363 | 349126.4 ±867.1 | 100 /0 |
| gets_grequests | 1.164 | 349100.5 ±806.0 | 100 /0 |

100次独立会话异步GET测试

URL: https://httpbin.org/get

| lib | total time(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| gets_aiohttp | 1.229 | 397.0 ±0.0 | 100 /0 |
| gets_grequests | 2.446 | 397.0 ±0.0 | 100 /0 |

100次独立会话异步GET测试

URL: https://dd.b.pvp.net/latest/set5/en_us/img/cards/05BC001.png

| lib | total time(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| gets_aiohttp | 2.289 | 588110.0 ±0.0 | 100 /0 |
| gets_grequests | 2.671 | 588110.0 ±0.0 | 100 /0 |

100次独立会话异步POST测试

URL/data: ('https://httpbin.org/post', {'a': 'A'})

| lib | total time(s) | mean bytes ±stdev | 200 /e |
| --- | --- | --- | --- |
| posts_aiohttp | 2.142 | 559.0 ±0.0 | 100 /0 |
| posts_grequests | 2.241 | 559.0 ±0.0 | 100 /0 |
