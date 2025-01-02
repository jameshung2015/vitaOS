from fastapi import UploadFile, HTTPException
from src.utils.file_processor import FileProcessor
from src.utils.ai_service import AIService
from src.utils.url_processor import URLProcessor
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class SummarizeService:
    def __init__(self):
        self.file_processor = FileProcessor()
        self.ai_service = AIService()
        self.url_processor = URLProcessor()
    
    async def summarize_url(self, url: str, api_key: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        总结 URL 内容
        :param url: 要总结的URL
        :param api_key: 可选的API密钥
        :param tags: 可选的标签列表
        :return: 包含总结和原URL的字典
        """
        try:
            # 获取 URL 内容
            content = await self.url_processor.get_url_content(url, tags)
            
            # 验证内容
            if not content or not content.strip():
                raise HTTPException(
                    status_code=400,
                    detail="URL内容为空"
                )
            
            # 记录内容长度
            logger.info(f"获取到URL内容，长度: {len(content)} 字符")
            logger.debug(f"内容前100个字符: {content[:100]}")
            
            # 使用 AI 服务生成总结
            summary = await self.ai_service.generate_summary(content, api_key)
            
            return {
                "summary": summary,
                "source_url": url
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"URL内容总结失败: {str(e)}"
            )
    
    async def summarize_file(self, file: UploadFile, api_key: Optional[str] = None) -> Dict[str, Any]:
        """
        总结文件内容
        :param file: 上传的文件
        :param api_key: 可选的API密钥
        :return: 包含总结和追问问题的字典
        """
        try:
            # 处理文件内容
            content = self.file_processor.extract_content(file.filename)
            
            # 使用 AI 服务生成总结
            summary = await self.ai_service.generate_summary(content, api_key)
            
            # 生成追问问题
            questions = await self.ai_service.generate_follow_up_questions(content, summary, api_key)
            
            return {
                "summary": summary,
                "follow_up_questions": questions
            }
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"文件内容总结失败: {str(e)}"
            ) 