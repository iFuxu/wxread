# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re

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

# 原始的headers、cookies和data，作为默认值
cookies = {
    'RK': 'oxEY1bTnXf',
    'ptcz': '53e3b35a9486dd63c4d06430b05aa169402117fc407dc5cc9329b41e59f62e2b',
    'pac_uid': '0_e63870bcecc18',
    'iip': '0',
    '_qimei_uuid42': '183070d3135100ee797b08bc922054dc3062834291',
    'wr_avatar': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FeEOpSbFh2Mb1bUxMW9Y3FRPfXwWvOLaNlsjWIkcKeeNg6vlVS5kOVuhNKGQ1M8zaggLqMPmpE5qIUdqEXlQgYg%2F132',
    'wr_gender': '0',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ko;q=0.5',
    'baggage': 'sentry-environment=production,sentry-release=dev-1730698697208,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=1ff5a0725f8841088b42f97109c45862',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}

data = {
    "appId": "wb182564874663h776775553",
    "b": "f623242072a191daf6294db",
    "c": "17c32d00329e17c276c8288",
    "ci": 137,
    "co": 7098,
    "sm": "其实领导也挺不好当的。”我笑了笑，说",
    "pr": 55,
    "rt": 30,
    "ts": 1739673850629,
    "rn": 412,
    "sg": "41b43c2f8b6b065530e28001b91c6f2ba36e70eb397ca016e891645bf18b27d8",
    "ct": 1739673850,
    "ps": "ca5326207a5e8814g01704b",
    "pc": "f2332e707a5e8814g0181e0",
}

def convert(curl_command):
    """提取bash接口中的headers与cookies
    支持 -H 'Cookie: xxx' 和 -b 'xxx' 两种方式的cookie提取
    """
    # 提取 headers
    headers_temp = {}
    for match in re.findall(r"-H '([^:]+): ([^']+)'", curl_command):
        headers_temp[match[0]] = match[1]

    # 提取 cookies
    cookies = {}
    
    # 从 -H 'Cookie: xxx' 提取
    cookie_header = next((v for k, v in headers_temp.items() 
                         if k.lower() == 'cookie'), '')
    
    # 从 -b 'xxx' 提取
    cookie_b = re.search(r"-b '([^']+)'", curl_command)
    cookie_string = cookie_b.group(1) if cookie_b else cookie_header
    
    # 解析 cookie 字符串
    if cookie_string:
        for cookie in cookie_string.split('; '):
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                cookies[key.strip()] = value.strip()
    
    # 移除 headers 中的 Cookie/cookie
    headers = {k: v for k, v in headers_temp.items() 
              if k.lower() != 'cookie'}

    return headers, cookies

# 使用新的curl命令更新headers和cookies
new_headers, new_cookies = convert(curl_str if curl_str else 'curl ' + 
'https://weread.qq.com/web/book/read' 
  +' -H \'accept: application/json, text/plain, */*\' '
  +' -H \'accept-language: zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6\' '
  +' -H \'baggage: sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=a933e810bcb84917bdcfb7488323db1d\' '
  +' -H \'content-type: application/json;charset=UTF-8\' '
  +' -b \'_clck=19i332h|1|ftt|0; wr_fp=813316764; wr_pf=0; wr_useHorizonReader=0; wr_vid=917243444; wr_rt=web%40n6skqK5Lkz_r9sCnvj3_AL; wr_localvid=92a32810836ac063492a86f; wr_name=%C2%A0; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FOcM3yyOe0qGkN6o1E9CdsLtKzJFk5sjBLAKtKjZsc8ejfHSWu4xC3WPthibRoJdZVia6j8bgpMKUMBoiaR0HicCl4nsAuVSTHxRxTYKxu8NBBFI%2F132; wr_gender=0; wr_skey=gMy6hMdJ; wr_gid=292659964\' '
  +' -H \'dnt: 1\' '
  +' -H \'origin: https://weread.qq.com\' '
  +' -H \'priority: u=1, i\' '
  +' -H \'referer: https://weread.qq.com/web/reader/a57325c05c8ed3a57224187k3fe32cd0313c3fe94a00ac6\' '
  +' -H \'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"\' '
  +' -H \'sec-ch-ua-mobile: ?0\' '
  +' -H \'sec-ch-ua-platform: "Windows"\' '
  +' -H \'sec-fetch-dest: empty\' '
  +' -H \'sec-fetch-mode: cors\' '
  +' -H \'sec-fetch-site: same-origin\' '
  +' -H \'sec-gpc: 1\' '
  +' -H \'sentry-trace: a933e810bcb84917bdcfb7488323db1d-9b666a64aa41aac9\' '
  +' -H \'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\' '
  +' --data-raw \'{"appId":"wb182564874663h1964571299","b":"a57325c05c8ed3a57224187","c":"3fe32cd0313c3fe94a00ac6","ci":316,"co":338,"sm":"第314章杨涟(1)天启四年(1624)","pr":100,"rt":9,"ts":1741939163852,"rn":889,"sg":"d2d73b99e3fcba8d0c3bea6ab4ebc2de9de6f4e79b423d9994196781ff05ad7e","ct":1741939163,"ps":"b13323b07a61fcfbg011ec6","pc":"e5932cd07a61fcfbg013cfd","s":"88ee39ee"}\'')
headers.update(new_headers)
cookies.update(new_cookies)

# 尝试提取data中的字段并更新到现有data中
try:
    data_str = re.search(r"--data-raw '({.*?})'", curl_str if curl_str else 'curl ' + 
'https://weread.qq.com/web/book/read' 
  +' -H \'accept: application/json, text/plain, */*\' '
  +' -H \'accept-language: zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6\' '
  +' -H \'baggage: sentry-environment=production,sentry-release=dev-1738835404736,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=a933e810bcb84917bdcfb7488323db1d\' '
  +' -H \'content-type: application/json;charset=UTF-8\' '
  +' -b \'_clck=19i332h|1|ftt|0; wr_fp=813316764; wr_pf=0; wr_useHorizonReader=0; wr_vid=917243444; wr_rt=web%40n6skqK5Lkz_r9sCnvj3_AL; wr_localvid=92a32810836ac063492a86f; wr_name=%C2%A0; wr_avatar=https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FOcM3yyOe0qGkN6o1E9CdsLtKzJFk5sjBLAKtKjZsc8ejfHSWu4xC3WPthibRoJdZVia6j8bgpMKUMBoiaR0HicCl4nsAuVSTHxRxTYKxu8NBBFI%2F132; wr_gender=0; wr_skey=gMy6hMdJ; wr_gid=292659964\' '
  +' -H \'dnt: 1\' '
  +' -H \'origin: https://weread.qq.com\' '
  +' -H \'priority: u=1, i\' '
  +' -H \'referer: https://weread.qq.com/web/reader/a57325c05c8ed3a57224187k3fe32cd0313c3fe94a00ac6\' '
  +' -H \'sec-ch-ua: "Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"\' '
  +' -H \'sec-ch-ua-mobile: ?0\' '
  +' -H \'sec-ch-ua-platform: "Windows"\' '
  +' -H \'sec-fetch-dest: empty\' '
  +' -H \'sec-fetch-mode: cors\' '
  +' -H \'sec-fetch-site: same-origin\' '
  +' -H \'sec-gpc: 1\' '
  +' -H \'sentry-trace: a933e810bcb84917bdcfb7488323db1d-9b666a64aa41aac9\' '
  +' -H \'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\' '
  +' --data-raw \'{"appId":"wb182564874663h1964571299","b":"a57325c05c8ed3a57224187","c":"3fe32cd0313c3fe94a00ac6","ci":316,"co":338,"sm":"第314章杨涟(1)天启四年(1624)","pr":100,"rt":9,"ts":1741939163852,"rn":889,"sg":"d2d73b99e3fcba8d0c3bea6ab4ebc2de9de6f4e79b423d9994196781ff05ad7e","ct":1741939163,"ps":"b13323b07a61fcfbg011ec6","pc":"e5932cd07a61fcfbg013cfd","s":"88ee39ee"}\'').group(1)
    new_data = eval(data_str)  # 注意eval有安全风险，可考虑使用json.loads替代并确保数据格式正确
    data.update(new_data)
except:
    print("无法正确解析curl命令中的data部分，使用默认配置")

headers, cookies = convert(curl_str) if curl_str else (headers, cookies)
