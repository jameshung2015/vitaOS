from openai import AsyncOpenAI
from typing import List, Optional
from src.utils.config_manager import ConfigManager
from src.utils.logger import get_logger

logger = get_logger("sumbot.ai_service")

class AIService:
    def __init__(self):
        self.config = ConfigManager()
        self.client = None
        self.model = None
    
    def _init_client(self, api_key: Optional[str] = None):
        """
        延迟初始化客户端
        优先使用传入的 api_key，否则使用配置中的密钥
        """
        try:
            ai_config = self.config.get_ai_service_config()
            service_name = ai_config.get('service')
            service_config = ai_config
            
            # 验证必要的配置项
            if not service_config.get('api_base'):
                raise ValueError(f"服务 {service_name} 未配置 api_base")
            if not service_config.get('model'):
                raise ValueError(f"服务 {service_name} 未配置 model")
            
            # 优先使用传入的 API 密钥
            if api_key:
                if not api_key.startswith('sk-'):
                    raise ValueError("API密钥必须以 'sk-' 开头")
                service_config['api_key'] = api_key
            elif not service_config.get('api_key'):
                # 如果没有提供 API 密钥且配置中也没有，使用默认密钥
                default_key = ai_config.get('default_api_key')
                if not default_key:
                    raise ValueError("未提供API密钥且未配置默认密钥")
                service_config['api_key'] = default_key
            
            # 创建客户端
            self.client = AsyncOpenAI(
                api_key=service_config['api_key'],
                base_url=service_config['api_base'],
                timeout=30.0
            )
            self.model = service_config['model']
            
            logger.debug(f"已初始化 {service_name} 客户端")
            logger.debug(f"使用模型: {self.model}")
            logger.debug(f"API Base URL: {service_config['api_base']}")
        except Exception as e:
            logger.error(f"初始化AI客户端失败: {str(e)}")
            raise
    
    async def generate_summary(self, content: str, api_key: Optional[str] = None) -> str:
        """
        生成内容总结
        :param content: 要总结的内容
        :param api_key: 可选的 API 密钥
        """
        if not self.client or api_key:
            self._init_client(api_key)
        
        try:
            # 记录请求信息
            logger.info("发送总结请求:")
            logger.info(f"模型: {self.model}")
            logger.info(f"内容长度: {len(content)} 字符")
            logger.info(f"API Base URL: {self.client.base_url}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的文章总结助手。请简洁明了地总结以下内容的要点："},
                    {"role": "user", "content": content}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # 记录响应信息
            logger.info("收到总结响应:")
            logger.info(f"响应状态: 成功")
            logger.info(f"总结长度: {len(response.choices[0].message.content)} 字符")
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"生成总结失败: {str(e)}")
            logger.error(f"错误类型: {type(e).__name__}")
            logger.error(f"错误详情: {str(e)}")
            raise Exception(f"生成总结失败: {str(e)}")
    
    async def generate_follow_up_questions(self, content: str, summary: str, api_key: Optional[str] = None) -> List[str]:
        """
        生成追问问题
        :param content: 原文内容
        :param summary: 总结内容
        :param api_key: 可选的 API 密钥
        """
        if not self.client or api_key:
            self._init_client(api_key)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "基于文章内容和总结，生成3个有见地的追问问题："},
                    {"role": "user", "content": f"文章内容：{content}\n\n总结：{summary}"}
                ],
                temperature=0.8,
                max_tokens=200
            )
            questions = response.choices[0].message.content.strip().split('\n')
            return [q.strip('1234567890. ') for q in questions if q.strip()]
        except Exception as e:
            logger.error(f"生成追问问题失败: {str(e)}")
            raise Exception(f"生成追问问题失败: {str(e)}") 