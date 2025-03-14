# main.py 主逻辑（增强版）
import re
import json
import time
import random
import logging
import hashlib
import requests
import urllib.parse
from push import push
from config import (
    data, headers, cookies,
    READ_NUM, PUSH_METHOD,
    b_values, random_b_value  # 使用新版config配置
)

# ================= 增强配置 =================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('WeReadBot')

# 安全参数配置
CRYPTO_KEY = os.getenv('CRYPTO_KEY', "3c5c8717f3daf09iop3423zafeqoi")  # 密钥可配置化
MAX_RETRY = 3  # 失败重试次数
RETRY_DELAY = 10  # 重试等待秒数

# ================= 核心函数 =================
class RequestEngine:
    """请求引擎（封装安全策略）"""
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.cookies.update(cookies)
        
    def secure_request(self, url, payload):
        """带安全策略的请求"""
        for attempt in range(MAX_RETRY):
            try:
                response = self.session.post(
                    url,
                    data=json.dumps(payload, separators=(',', ':')),
                    timeout=15
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                logger.warning(f"请求失败（尝试 {attempt+1}/{MAX_RETRY}）: {str(e)}")
                time.sleep(RETRY_DELAY * (attempt + 1))
        return None

# ================= 加密模块 =================
class CryptoUtils:
    @staticmethod
    def generate_signature(payload_data):
        """生成请求签名"""
        encoded_str = '&'.join(
            f"{k}={urllib.parse.quote(str(payload_data[k]), safe='')}"
            for k in sorted(payload_data.keys())
        )
        return CryptoUtils._calculate_hash(encoded_str)
    
    @staticmethod
    def _calculate_hash(input_str):
        """改良哈希算法"""
        hash_base = 0x15051505
        length = len(input_str)
        for i in range(length - 1, -1, -2):
            hash_base = (hash_base ^ (ord(input_str[i]) << ((length - i) % 30))) & 0x7fffffff
        return f"{hash_base:x}".zfill(8)

# ================= 业务逻辑 =================
def refresh_session_key():
    """刷新会话密钥（带熔断机制）"""
    try:
        response = requests.post(
            "https://weread.qq.com/web/login/renewal",
            headers=headers,
            cookies=cookies,
            json={"rq": "%2Fweb%2Fbook%2Fread"}
        )
        new_cookie = next(
            (cookie.split('=')[1] for cookie in response.headers.get('Set-Cookie', '').split('; ')
             if 'wr_skey' in cookie),
            None
        )
        if new_cookie:
            cookies['wr_skey'] = new_cookie.split(';')[0]
            logger.info(f"会话密钥已更新: {new_cookie[:8]}...")
            return True
        return False
    except Exception as e:
        logger.error(f"密钥刷新失败: {str(e)}")
        return False

def build_payload():
    """动态构建请求负载"""
    timestamp = int(time.time())
    payload = data.copy()
    payload.update({
        'b': random.choice(b_values),  # 每次请求随机选书
        'ct': timestamp,
        'ts': timestamp * 1000,
        'rn': random.randint(1000, 9999),
        'sg': hashlib.sha256(f"{timestamp}{CRYPTO_KEY}".encode()).hexdigest()
    })
    payload['s'] = CryptoUtils.generate_signature(payload)
    return payload

# ================= 主执行流 =================
if __name__ == "__main__":
    req_engine = RequestEngine()
    total_read = 0
    
    for count in range(1, READ_NUM + 1):
        payload = build_payload()
        logger.info(f"📖 第 {count}/{READ_NUM} 次阅读 | 书籍: {payload['b']}")
        
        response = req_engine.secure_request(
            "https://weread.qq.com/web/book/read",
            payload
        )
        
        if response and response.get('succ'):
            total_read += 1
            logger.info(f"✅ 阅读成功 (累计 {total_read} 次)")
            time.sleep(random.uniform(25, 35))  # 随机间隔防检测
        else:
            logger.warning("⚠️ 阅读失败，尝试刷新会话...")
            if refresh_session_key():
                req_engine.session.cookies.update(cookies)
                count -= 1  # 重试当前次数
            else:
                error_msg = "❌ 会话刷新失败，终止程序"
                logger.error(error_msg)
                push(error_msg, PUSH_METHOD)
                break
        
        if 's' in payload:
            del payload['s']  # 清理敏感字段
    
    # 最终结果推送
    if total_read > 0:
        success_msg = f"🎉 成功阅读 {total_read} 次 (约 {total_read*0.5} 分钟)"
        logger.info(success_msg)
        if PUSH_METHOD:
            push(success_msg, PUSH_METHOD)
