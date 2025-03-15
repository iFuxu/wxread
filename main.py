# main.py 主逻辑：包括字段拼接、模拟请求
import re
import json
import time
import random
import logging
import requests
from config import data, headers, cookies, READ_TIME, PUSH_METHOD, PROXY
from crypto import Encryptor
from push import push

# 配置日志格式
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)-8s - %(message)s')

# 初始化加密器
encryptor = Encryptor(KEY)

# 加密盐及其它默认值
COOKIE_DATA = {"rq": "%2Fweb%2Fbook%2Fread"}
READ_URL = "https://weread.qq.com/web/book/read"
RENEW_URL = "https://weread.qq.com/web/login/renewal"

MAX_RETRIES = 3  # 新增重试次数


def get_wr_skey():
    """刷新cookie密钥并添加重试机制"""
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.post(RENEW_URL, headers=headers, cookies=cookies,
                                     data=json.dumps(COOKIE_DATA, separators=(',', ':')))
            for cookie in response.headers.get('Set-Cookie', '').split(';'):
                if "wr_skey" in cookie:
                    return cookie.split('=')[-1][:8]
            logging.warning(f"尝试 {attempt + 1}/{MAX_RETRIES} 失败，无有效cookie")
        except Exception as e:
            logging.error(f"请求失败: {str(e)}")
        time.sleep(5)  # 每次重试间隔
    return None


def mask_sensitive_info(info):
    """对敏感信息进行掩码处理"""
    if 'wr_skey' in info:
        info['wr_skey'] = info['wr_skey'][:4] + '****'
    return info


def get_read_strategy():
    """根据时间段调整阅读策略"""
    current_hour = time.localtime().tm_hour
    if 22 <= current_hour < 6:
        return {
            'base_time': 30,
            'float_time': 15,
            'pause_chance': 0.2
        }
    else:
        return {
            'base_time': 60,
            'float_time': 30,
            'pause_chance': 0.3
        }


def cleanup():
    """执行后的资源清理"""
    logging.info("执行清理操作...")
    # 可以添加临时文件删除、缓存清理等操作


if __name__ == "__main__":
    try:
        strategy = get_read_strategy()
        max_index = int(READ_TIME * 2)
        pause_chance = strategy['pause_chance']

        index = 1
        while index <= max_index:
            data['ct'] = int(time.time())
            data['ts'] = int(time.time() * 1000)
            data['rn'] = random.randint(0, 1000)
            data['sg'] = hashlib.sha256(f"{data['ts']}{data['rn']}{KEY}".encode()).hexdigest()
            data['s'] = encryptor.cal_hash(encryptor.encode_data(data))

            logging.info(f"⏱️ 尝试第 {index} 次阅读...")
            try:
                response = requests.post(
                    READ_URL,
                    headers=headers,
                    cookies=cookies,
                    data=json.dumps(data, separators=(',', ':')),
                    proxies={'http': PROXY, 'https': PROXY} if PROXY else None,
                    timeout=10  # 新增超时设置
                )
            except requests.exceptions.RequestException as e:
                logging.error(f"网络请求失败: {str(e)}")
                # 可以选择重试或终止
                raise

            resData = response.json()
            logging.debug(f"原始响应数据: {resData}")  # 需要设置日志级别为DEBUG

            if'succ' in resData:
                index += 1
                time.sleep(30)
                logging.info(f"✅ 阅读成功，阅读进度：{(index - 1) * 0.5} 分钟")

                # 随机决定是否暂停
                if random.random() < pause_chance:  # 按策略暂停
                    pause_duration = random.randint(1, 3)  # 随机暂停 1 - 3 分钟
                    logging.info(f"暂停阅读，持续 {pause_duration} 分钟")
                    time.sleep(pause_duration * 60)

            else:
                logging.warning("❌ cookie 已过期，尝试刷新...")
                new_skey = get_wr_skey()
                if new_skey:
                    cookies['wr_skey'] = new_skey
                    logging.info(f"✅ 密钥刷新成功，新密钥：{new_skey}")
                    logging.info(f"🔄 重新本次阅读。")
                else:
                    ERROR_CODE = "❌ 无法获取新密钥或者WXREAD_CURL_BASH配置有误，终止运行。"
                    logging.error(ERROR_CODE)
                    push(ERROR_CODE, PUSH_METHOD)
                    raise Exception(ERROR_CODE)
            data.pop('s')

        logging.info("🎉 阅读脚本已完成！")

        if PUSH_METHOD not in (None, ''):
            logging.info("⏱️ 开始推送...")
            push(f"🎉 老微信已完成！\n⏱️ 阅读时长：{READ_TIME}分钟。", PUSH_METHOD)
    except Exception as e:
        logging.error(f"程序异常终止: {str(e)}")
    finally:
        cleanup()
