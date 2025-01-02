import os
import logging
from datetime import datetime

class Logger:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._setup_logging()
    
    def _setup_logging(self):
        """配置日志记录"""
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # 获取当前日期的日志文件路径
        log_file = os.path.join(log_dir, f"sumbot_{datetime.now().strftime('%Y%m%d')}.log")
        
        # 配置根日志记录器
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # 配置uvicorn和FastAPI日志记录器
        for logger_name in ["uvicorn", "uvicorn.access", "fastapi", "sumbot"]:
            logger = logging.getLogger(logger_name)
            logger.handlers = logging.getLogger().handlers
    
    def get_logger(self, name="sumbot"):
        """获取指定名称的日志记录器"""
        return logging.getLogger(name)

# 创建全局日志记录器实例
logger = Logger()

def get_logger(name="sumbot"):
    """获取日志记录器的便捷方法"""
    return logger.get_logger(name) 