import os
import sys
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1.endpoints.summarize import router as summarize_router
from utils.config_manager import ConfigManager
from utils.logger import get_logger
import time
import json

# 添加项目根目录到Python路径
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# 加载配置
config = ConfigManager()
api_config = config.get_api_config()

# 获取日志记录器
logger = get_logger("sumbot.api")

app = FastAPI(
    title=api_config.get('name', 'SumBot API'),
    description="文章总结和问答服务",
    version=api_config.get('version', 'v1')
)

# 添加日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 记录请求开始
    start_time = time.time()
    
    # 记录请求体
    body = await request.body()
    if body:
        try:
            body_str = body.decode()
            if request.headers.get('content-type') == 'application/json':
                body_json = json.loads(body_str)
                logger.info(f"请求体: {json.dumps(body_json, ensure_ascii=False)}")
            else:
                logger.info(f"请求体: {body_str}")
        except Exception as e:
            logger.error(f"解析请求体失败: {str(e)}")
    
    # 记录请求头
    headers = dict(request.headers)
    logger.info(f"请求头: {json.dumps(headers, ensure_ascii=False)}")
    
    response = await call_next(request)
    
    # 计算处理时间
    process_time = (time.time() - start_time) * 1000
    
    # 记录请求信息
    logger.info(
        f"{request.client.host}:{request.client.port} - "
        f"\"{request.method} {request.url.path} HTTP/{request.scope.get('http_version', '1.1')}\" "
        f"{response.status_code} - {process_time:.2f}ms"
    )
    
    return response

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(summarize_router)

@app.get("/")
async def root():
    """
    API 根路径
    """
    return {
        "message": f"欢迎使用 {api_config.get('name', 'SumBot')} API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }