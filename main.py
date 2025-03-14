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

# 配置日志格式，增加日期时间的详细程度和毫秒级显示
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d - %(levelname)-8s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 定义常量，使代码更清晰易读
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"


def encode_data(data):
    """
    对传入的数据进行编码处理
    :param data: 包含请求参数的字典数据
    :return: 编码后的参数字符串
    """
    return '&'.join(f"{k}={urllib.parse.quote(str(data[k]), safe='')}" for k in sorted(data.keys()))


def cal_hash(input_string):
    """
    计算输入字符串的哈希值
    :param input_string: 待计算哈希值的字符串
    :return: 计算得到的哈希值（十六进制字符串形式）
    """
    hash_value_1 = 0x15051505
    hash_value_2 = hash_value_1
    length = len(input_string)
    string_index = length - 1

    while string_index > 0:
        hash_value_1 = 0x7fffffff & (hash_value_1 ^ ord(input_string[string_index]) << (length - string_index) % 30)
        hash_value_2 = 0x7fffffff & (hash_value_2 ^ ord(input_string[string_index - 1]) << string_index % 30)
        string_index -= 2

    return hex(hash_value_1 + hash_value_2)[2:].lower()


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

        if'succ' in resData:
            index += 1
            time.sleep(30)
            logging.info(f"✅ 阅读成功，阅读进度：{(index - 1) * 0.5} 分钟")
            retry_count = 0
        else:
            error_msg = "❌ cookie 已过期或请求数据有误，终止运行。"
            logging.error(error_msg)
            if PUSH_METHOD not in (None, ''):
                push(error_msg, PUSH_METHOD)
            raise Exception(error_msg)
    except requests.RequestException as e:
        logger.error(f"阅读请求失败: {e}，请求URL: {READ_URL}，请求头: {headers}，请求cookies: {cookies}，请求数据: {data}，正在重试...")
        retry_count += 1
        if retry_count >= max_retry:
            logging.error(f"达到最大重试次数 {max_retry}，放弃本次阅读请求。")
            break
        time.sleep(5)
        continue
    except json.JSONDecodeError as e:
        try:
            response_text = response.text if response else "无响应内容"
            logger.error(f"解析阅读响应失败: {e}，响应内容: {response_text}，正在重试...")
        except:
            logger.error(f"解析阅读响应失败: {e}，无响应内容可获取，正在重试...")
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
else:
    logging.info("未设置推送方法，跳过推送操作。")
