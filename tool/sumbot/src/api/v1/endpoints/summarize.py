from fastapi import APIRouter, HTTPException, UploadFile, File, Request
from typing import Optional
from src.schemas.summarize import (
    URLSummarizeRequest,
    URLSummarizeResponse,
    SearchSummarizeRequest,
    SearchSummarizeResponse
)
from src.services.summarize import SummarizeService
from src.utils.logger import get_logger
import json

router = APIRouter(
    prefix="/api/v1/summarize",
    tags=["summarize"]
)

summarize_service = SummarizeService()
logger = get_logger("sumbot.api.summarize")

@router.post("/url", response_model=URLSummarizeResponse)
async def summarize_url(request: URLSummarizeRequest, req: Request):
    """
    总结URL内容
    """
    try:
        # 记录详细的请求信息
        logger.info("收到URL总结请求:")
        logger.info(f"URL: {request.url}")
        logger.info(f"标签: {request.tags}")
        logger.info(f"最大长度: {request.max_length}")
        logger.info(f"客户端IP: {req.client.host}")
        logger.info(f"请求方法: {req.method}")
        logger.info(f"请求路径: {req.url.path}")
        
        # 记录请求头
        headers = dict(req.headers)
        logger.info(f"请求头: {json.dumps(headers, ensure_ascii=False)}")
        
        # 将HttpUrl转换为字符串
        url_str = str(request.url)
        result = await summarize_service.summarize_url(url_str, request.api_key, request.tags)
        logger.info("URL总结完成")
        return URLSummarizeResponse(
            summary=result["summary"],
            source_url=result["source_url"]
        )
    except Exception as e:
        logger.error(f"URL总结失败: {str(e)}")
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"错误详情: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/file")
async def summarize_file(file: UploadFile = File(...)):
    """
    总结文件内容
    """
    try:
        result = await summarize_service.summarize_file(file)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/image")
async def analyze_image(image: UploadFile = File(...)):
    """
    分析图片内容
    """
    try:
        result = await summarize_service.analyze_image(image)
        return {"analysis": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/video")
async def summarize_video(url: str):
    """
    总结视频内容
    """
    try:
        result = await summarize_service.summarize_video(url)
        return {"summary": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/search", response_model=SearchSummarizeResponse)
async def search_and_summarize(request: SearchSummarizeRequest):
    """
    搜索并总结内容
    """
    try:
        result = await summarize_service.search_and_summarize(request.query)
        return SearchSummarizeResponse(summary=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 