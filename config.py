1| # config.py 自定义配置,包括阅读次数、推送token的填写
2| import os
3| import re
4| 
5| """
6| 可修改区域
7| 默认使用本地值如果不存在从环境变量中获取值
8| """
9| 
10| # 阅读次数 默认120次/60分钟
11| READ_NUM = int(os.getenv('READ_NUM') or 120)
12| # 需要推送时可选，可选pushplus、wxpusher、telegram
13| PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
14| # pushplus推送时需填
15| PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
16| # telegram推送时需填
17| TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
18| TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
19| # wxpusher推送时需填
20| WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
21| # read接口的bash命令，本地部署时可对应替换headers、cookies
22| curl_str = os.getenv('WXREAD_CURL_BASH')
23| 
24| # headers、cookies是一个省略模版，本地或者docker部署时对应替换
25| cookies = {
26|     'RK': 'oxEY1bTnXf',
27|     'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
28|     'pac_uid': '0_e63870bcecc18',
29|     'iip': '0',
30|     '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
31|     'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEI0jgnTicYkV683eVjqcD9xno9xU7sjXBEQkJgALm1q7iaAhTiaJ67cicOvibXP77OgAMubcaY6b8VESAEkZXYGnM5M8pIuVBsrcv8ruZWfOQ3HmPQ%2F1[...]
32|     'wr_gender': '0',
33| }
34| 
35| headers = {
36|     'accept': 'application/json, text/plain, */*',
37|     'accept-language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
38|     'baggage': 'sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=87a995ae4d044168ae850d05136e9262',
39|     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
40| }
41| 
42| 
43| """
44| 建议保留区域|默认读三体，其它书籍自行测试时间是否增加
45| """
46| # config.py 自定义配置,包括阅读次数、推送token的填写
47| import os
48| import re
49| import json
50| 
51| """
52| 可修改区域
53| 默认使用本地值如果不存在从环境变量中获取值
54| """
55| 
56| # 阅读次数 默认120次/60分钟
57| READ_NUM = int(os.getenv('READ_NUM') or 120)
58| # 需要推送时可选，可选pushplus、wxpusher、telegram
59| PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
60| # pushplus推送时需填
61| PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
62| # telegram推送时需填
63| TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
64| TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
65| # wxpusher推送时需填
66| WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
67| # read接口的bash命令，本地部署时可对应替换headers、cookies
68| curl_str = os.getenv('WXREAD_CURL_BASH')
69| 
70| # headers、cookies是一个省略模版，本地或者docker部署时对应替换
71| cookies = {
72|     'RK': 'oxEY1bTnXf',
73|     'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
74|     'pac_uid': '0_e63870bcecc18',
75|     'iip': '0',
76|     '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
77|     'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEI0jgnTicYkV683eVjqcD9xno9xU7sjXBEQkJgALm1q7iaAhTiaJ67cicOvibXP77OgAMubcaY6b8VESAEkZXYGnM5M8pIuVBsrcv8ruZWfOQ3HmPQ%2F1[...]
78|     'wr_gender': '0',
79| }
80| 
81| headers = {
82|     'accept': 'application/json, text/plain, */*',
83|     'accept-language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
84|     'baggage': 'sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=87a995ae4d044168ae850d05136e9262',
85|     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
86| }
87| 
88| 
89| """
90| 建议保留区域|默认读三体，其它书籍自行测试时间是否增加
91| """
92| data_dict = {
93|     "appId": "wb182564874663h1964571299",
94|     "b": "3a8321c0813ab7839g011bd5",
95|     "c": "c7432af0210c74d97b01b1c",
96|     "ci": 16,
97|     "co": 14704,
98|     "sm": "按：周家仁厚立国，规模已定，惟商民犹伺隙",
99|     "pr": 0,
100|     "rt": 9,
101|     "ts": 1742019929869,
102|     "rn": 401,
103|     "sg": "36ba83886f1cb5ebbca0120a79e8954dec72ab8b029126cfa6e6abfb878a0205",
104|     "ct": 1742019929,
105|     "ps": "6c832b107a621c87g01145f",
106|     "pc": "fdc325e07a621c87g0129cc"
107| }
108| 
109| data = json.dumps(data_dict)
110| 
111| def convert(curl_command):
112|     """提取bash接口中的headers与cookies
113|     支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
114|     """
115|     # 提取 headers
116|     headers_temp = {}
117|     for match in re.findall(r'-H \'([^:]+): ([^\']+)\'', curl_command):
118|         headers_temp[match[0]] = match[1]
119| 
120|     # 提取 cookies
121|     cookies = {}
122| 
123|     # 从 -H 'Cookie: xxx' 提取  
124|     cookie_header = next((v for k, v in headers_temp.items()
125|                           if k.lower() == 'cookie'), '')
126| 
127|     # 从 -b 'xxx' 提取
128|     cookie_b = re.search(r'-b \'([^\']+)\'', curl_command)
129|     cookie_string = cookie_b.group(1) if cookie_b else cookie_header
130| 
131|     # 解析 cookie 字符串
132|     if cookie_string:
133|         for cookie in cookie_string.split('; '):
134|             if '=' in cookie:
135|                 key, value = cookie.split('=', 1)
136|                 cookies[key.strip()] = value.strip()
137| 
138|     # 移除 headers 中的 Cookie/cookie
139|     headers = {k: v for k, v in headers_temp.items()
140|                if k.lower() != 'cookie'}
141| 
142|     return headers, cookies
143| 
144| 
145| headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
146| 
147| def convert(curl_command):
148|     """提取bash接口中的headers与cookies
149|     支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
150|     """
151|     # 提取 headers
152|     headers_temp = {}
153|     for match in re.findall(r'-H \'([^:]+): ([^\']+)\'', curl_command):
154|         headers_temp[match[0]] = match[1]
155| 
156|     # 提取 cookies
157|     cookies = {}
158| 
159|     # 从 -H 'Cookie: xxx' 提取  
160|     cookie_header = next((v for k, v in headers_temp.items()
161|                           if k.lower() == 'cookie'), '')
162| 
163|     # 从 -b 'xxx' 提取
164|     cookie_b = re.search(r'-b \'([^\']+)\'', curl_command)
165|     cookie_string = cookie_b.group(1) if cookie_b else cookie_header
166| 
167|     # 解析 cookie 字符串
168|     if cookie_string:
169|         for cookie in cookie_string.split('; '):
170|             if '=' in cookie:
171|                 key, value = cookie.split('=', 1)
172|                 cookies[key.strip()] = value.strip()
173| 
174|     # 移除 headers 中的 Cookie/cookie
175|     headers = {k: v for k, v in headers_temp.items()
176|                if k.lower() != 'cookie'}
177| 
178|     return headers, cookies
179| 
180| 
181| headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
182| 
