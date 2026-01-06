from pathlib import Path
from loguru import logger

# 创建日志目录
Path("logs").mkdir(parents=True, exist_ok=True)
# logger实例配置
logger.add("logs/douyin_downloader_{time:YYYY-MM-DD}.log", encoding='utf-8', rotation="00:00", compression="zip", enqueue=True, colorize=False)
logger.add("logs/douyin_downloader_{time:YYYY-MM-DD}.log.error", encoding='utf-8', rotation="00:00", compression="zip", enqueue=True, colorize=False)
