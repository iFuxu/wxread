# 使用更轻量级且更安全的基础镜像，python:3.10-slim 已经比较轻量，可考虑使用 Alpine 版本进一步减小体积，但可能需要处理一些依赖差异
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置时区为中国时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 cron
# 建议固定 cron 版本，避免因版本更新引入兼容性问题
RUN apt-get update && apt-get install -y cron=3.0pl1-135 && rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/local/bin:${PATH}"

# 复制项目文件
# 建议先复制 requirements.txt（如果有） 并安装依赖，再复制其他文件，这样可以利用 Docker 缓存，加快构建速度
COPY main.py push.py config.py ./

# 创建日志目录并设置权限
RUN mkdir -p /app/logs && chmod 777 /app/logs

# 安装 Python 依赖
# 建议使用 requirements.txt 文件管理依赖，这样更方便维护和复现依赖环境
# 同时添加 --upgrade 选项确保安装最新版本的依赖（根据实际需求调整）
RUN pip install --no-cache-dir --upgrade \
    requests>=2.32.3 \
    urllib3>=2.2.3

# 创建 cron 任务（每天凌晨1点执行）
# 使用更规范的日期格式化，避免潜在的格式问题
RUN echo "0 1 * * * cd /app && /usr/local/bin/python3 main.py >> /app/logs/$(date +\%Y-\%m-\%d).log 2>&1" > /etc/cron.d/wxread-cron
RUN chmod 0644 /etc/cron.d/wxread-cron
RUN crontab /etc/cron.d/wxread-cron

# 启动命令
# 建议使用更标准的 cron 启动方式，并且可以考虑输出 cron 日志以便调试
CMD ["sh", "-c", "service cron start && tail -f /var/log/cron.log"]

