# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re
import json

"""
可修改区域
默认使用本地值如果不存在从环境变量中获取值
"""

# 阅读次数 默认120次/60分钟
READ_NUM = int(os.getenv('READ_NUM') or 120)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = "" or os.getenv('PUSH_METHOD')
# pushplus推送时需填
PUSHPLUS_TOKEN = "" or os.getenv("PUSHPLUS_TOKEN")
# telegram推送时需填
TELEGRAM_BOT_TOKEN = "" or os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = "" or os.getenv("TELEGRAM_CHAT_ID")
# wxpusher推送时需填
WXPUSHER_SPT = "" or os.getenv("WXPUSHER_SPT")
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = os.getenv('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
cookies = {
    'RK': 'oxEY1bTnXf',
    'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
    'pac_uid': '0_e63870bcecc18',
    'iip': '0',
    '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FPiajxSqBRaEI0jgnTicYkV683eVjqcD9xno9xU7sjXBEQkJgALm1q7iaAhTiaJ67cicOvibXP77OgAMubcaY6b8VESAEkZXYGnM5M8pIuVBsrcv8ruZWfOQ3HmPQ%2F1Jg',
    'wr_gender': '0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'baggage': 'sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=87a995ae4d044168ae850d05136e9262',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""

data_dict = {
    "appId": "wb182564874663h1964571299",
    "b": "3a8321c0813ab7839g011bd5",
    "c": "c7432af0210c74d97b01b1c",
    "ci": 16,
    "co": 14704,
    "sm": "按：周家仁厚立国，规模已定，惟商民犹伺隙",
    "pr": 0,
    "rt": 9,
    "ts": 1742019929869,
    "rn": 401,
    "sg": "36ba83886f1cb5ebbca0120a79e8954dec72ab8b029126cfa6e6abfb878a0205",
    "ct": 1742019929,
    "ps": "6c832b107a621c87g01145f",
    "pc": "fdc325e07a621c87g0129cc"
}

data = json.dumps(data_dict)

def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r'-H \'([^:]+): ([^\']+)\'', curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}

    # 从 -H 'Cookie: xxx' 提取  
    cookie_header = next((v for k, v in headers_temp.items() if k.lower() == 'cookie'), '')

    # 从 -b 'xxx' 提取
    cookie_b = re.search(r'-b \'([^\']+)\'', curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header

    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()

    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() if k.lower() != 'cookie'}

    return headers, cookies

headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
