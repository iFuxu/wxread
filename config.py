# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re
import logging

# 配置日志格式，增加日期时间的详细程度和毫秒级显示
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)-8s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# 检查环境变量是否存在的辅助函数
def check_env_variable(var_name):
    var_value = os.getenv(var_name)
    if var_value is None:
        logger.error(f"未获取到环境变量 {var_name}")
    else:
        logger.info(f"获取到的环境变量 {var_name} 值为: {var_value}")
    return var_value


# 阅读次数 默认120次/60分钟
READ_NUM = int(check_env_variable('READ_NUM') or 120)
# 需要推送时可选，可选pushplus、wxpusher、telegram
PUSH_METHOD = check_env_variable('PUSH_METHOD') or ""
# pushplus推送时需填
PUSHPLUS_TOKEN = check_env_variable("PUSHPLUS_TOKEN") or ""
# telegram推送时需填
TELEGRAM_BOT_TOKEN = check_env_variable("TELEGRAM_BOT_TOKEN") or ""
TELEGRAM_CHAT_ID = check_env_variable("TELEGRAM_CHAT_ID") or ""
# wxpusher推送时需填
WXPUSHER_SPT = check_env_variable("WXPUSHER_SPT") or ""
# read接口的bash命令，本地部署时可对应替换headers、cookies
curl_str = check_env_variable('WXREAD_CURL_BASH')

# headers、cookies是一个省略模版，本地或者docker部署时对应替换
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
    'baggage':'sentry-environment=production,sentry-release=dev-1730698697208,sentry-public_key=ed67ed71f7804a038e898ba54bd66e44,sentry-trace_id=1ff5a0725f8841088b42f97109c45862',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
}


"""
建议保留区域|默认读三体，其它书籍自行测试时间是否增加
"""
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
    "ct": 1739673850,
    "ps": "ca5326207a5e8814g01704b",
    "pc": "f2332e707a5e8814g0181e0",
}


def convert(curl_command):
    """
    从curl命令字符串中提取出headers与cookies信息
    :param curl_command: curl命令字符串
    :return: 提取到的headers和cookies字典
    """
    headers_temp = {}
    cookies_temp = {}

    # 提取headers
    header_matches = re.findall(r'-H \'([^:]+): ([^']+)\'', curl_command)
    for header in header_matches:
        headers_temp[header[0]] = header[1]

    # 提取cookies
    cookie_matches = re.findall(r'(?:-b \'|; )([^;]+?)\'', curl_command)
    for cookie in cookie_matches:
        parts = cookie.split('=')
        if len(parts) == 2:
            cookies_temp[parts[0].strip()] = parts[1].strip()

    # 合并并更新全局的headers和cookies
    headers.update(headers_temp)
    cookies.update(cookies_temp)

    return headers, cookies


if curl_str:
    headers, cookies = convert(curl_str)
else:
    logger.warning("未获取到WXREAD_CURL_BASH，使用默认的headers和cookies")

# 打印提取后的headers和cookies，用于调试
logger.info("提取后的headers: %s", headers)
logger.info("提取后的cookies: %s", cookies)

