# main.py 主逻辑：包括字段拼接、模拟请求
import re
import json
import time
import random
import logging
import requests
import urllib.parse
from push import push
from config import data, headers, cookies, READ_NUM, PUSH_METHOD

# 配置日志格式，增加日期时间的详细程度
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)-8s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"


def encode_data(data):
    """数据编码"""
    return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))


def cal_hash(input_string):
    """计算哈希值"""
    _7032f5 = 0x15051505
    _cc1055 = _7032f5
    length = len(input_string)
    _19094e = length - 1

    while _19094e > 0:
        _7032f5 = 0x7fffffff & (_7032f5 ^ ord(input_string[_19094e]) << (length - _19094e) % 30)
        _cc1055 = 0x7fffffff & (_cc1055 ^ ord(input_string[_19094e - 1]) << _19094e % 30)
        _19094e -= 2

    return hex(_7032f5 + _cc1055)[2:].lower()


def get_wr_skey():
    """刷新cookie密钥"""
    try:
        response = requests.post(
            RENEW_URL,
            headers=headers,
            cookies=cookies,
            data=json.dumps(COOKIE_DATA, separators=(',', ':')),
            timeout=10
        )
        response.raise_for_status()  # 检查请求是否成功，失败则抛出异常
        logger.info(f"获取wr_skey的响应状态码: {response.status_code}")
        logger.info(f"获取wr_skey的响应头: {response.headers}")
        for cookie in response.headers.get('Set-Cookie', '').split(';'):
            if "wr_skey" in cookie:
                return cookie.split('=')[-1][:8]
        logger.warning("未在响应中找到wr_skey，响应头信息: %s", response.headers)
        return None
    except requests.RequestException as e:
        logger.error("获取wr_skey时请求失败: %s", e)
        return None


index = 1
retry_count = 0
max_retry = 3
while index <= READ_NUM:
    data['ct'] = int(time.time())
    data['ts'] = int(time.time() * 1000)
    data['rn'] = random.randint(0, 1000)
    data['s'] = cal_hash(encode_data(data))

    logging.info(f"⏱️ 尝试第 {index} 次阅读...")
    try:
        response = requests.post(
            READ_URL,
            headers=headers,
            cookies=cookies,
            data=json.dumps(data, separators=(',', ':')),
            timeout=10
        )
        response.raise_for_status()
        resData = response.json()

        if 'succ' in resData:
            index += 1
            time.sleep(30)
            logging.info(f"✅ 阅读成功，阅读进度：{(index - 1) * 0.5} 分钟")
            retry_count = 0
        else:
            logging.warning("❌ cookie 已过期，尝试刷新...")
            new_skey = get_wr_skey()
            if new_skey:
                cookies['wr_skey'] = new_skey
                logging.info(f"✅ 密钥刷新成功，新密钥：{new_skey}")
                logging.info(f"🔄 重新本次阅读。")
            else:
                error_msg = "❌ 无法获取新密钥或者WXREAD_CURL_BASH配置有误，终止运行。"
                logging.error(error_msg)
                if PUSH_METHOD not in (None, ''):
                    push(error_msg, PUSH_METHOD)
                raise Exception(error_msg)
    except requests.RequestException as e:
        logging.error(f"阅读请求失败: {e}，正在重试...")
        retry_count += 1
        if retry_count >= max_retry:
            logging.error(f"达到最大重试次数 {max_retry}，放弃本次阅读请求。")
            break
        time.sleep(5)
        continue
    except json.JSONDecodeError as e:
        logging.error(f"解析阅读响应失败: {e}，正在重试...")
        retry_count += 1
        if retry_count >= max_retry:
            logging.error(f"达到最大重试次数 {max_retry}，放弃本次阅读请求。")
            break
        time.sleep(5)
        continue
    finally:
        data.pop('s')

logging.info("🎉 阅读脚本已完成！")

if PUSH_METHOD not in (None, ''):
    logging.info("⏱️ 开始推送...")
    push(f"🎉 微信读书自动阅读完成！\n⏱️ 阅读时长：{(index - 1) * 0.5}分钟。", PUSH_METHOD)
