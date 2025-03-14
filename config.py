# config.py 自定义配置,包括阅读次数、推送token的填写
import os
import re
import random
from dotenv import load_dotenv

load_dotenv()

# ================= 核心配置 =================
def load_env_or_raise(key):
    """强制要求的环境变量加载"""
    value = os.getenv(key)
    if not value:
        raise ValueError(f"必须配置环境变量 {key}")
    return value

# 书籍ID列表（必须通过环境变量配置）
try:
    b_values = [bid.strip() for bid in load_env_or_raise('B_VALUES').split(',')]
    print(f"[CONFIG] 已加载 {len(b_values)} 个书籍ID")
except ValueError as e:
    # 兼容旧版curl解析逻辑
    curl_str = os.getenv('WXREAD_CURL_BASH')
    if curl_str:
        match = re.search(r"-H 'b: ([^']+)'", curl_str)
        if match:
            b_values = [match.group(1)]
            print(f"[CONFIG] 从curl命令解析到书籍ID: {b_values[0]}")
    else:
        raise

# ================= 推送配置 =================
PUSH_CONFIG = {
    "method": os.getenv('PUSH_METHOD'),
    "pushplus": os.getenv('PUSHPLUS_TOKEN'),
    "telegram": {
        "bot_token": os.getenv('TELEGRAM_BOT_TOKEN'),
        "chat_id": os.getenv('TELEGRAM_CHAT_ID')
    },
    "wxpusher": os.getenv('WXPUSHER_SPT')
}

# ================= 执行参数 =================
RUN_PARAMS = {
    "read_num": int(os.getenv('READ_NUM', 180)),  # 默认180次/90分钟
    "interval": random.randint(28, 32)            # 28-32秒随机间隔
}

print(f"[CONFIG] 运行参数: {RUN_PARAMS}")
