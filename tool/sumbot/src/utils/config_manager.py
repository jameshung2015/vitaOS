import json
import os
from typing import Any, Dict, Optional

class ConfigManager:
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'config.json'
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        except Exception as e:
            raise Exception(f"加载配置文件失败: {str(e)}")
    
    def get_api_config(self) -> Dict[str, Any]:
        """获取API配置"""
        return self._config.get('api', {})
    
    def get_ai_service_config(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """
        获取AI服务配置
        :param service_name: 服务名称，如果不指定则返回默认服务的配置
        :return: AI服务配置
        :raises: Exception 如果找不到配置或配置无效
        """
        ai_config = self._config.get('ai_service', {})
        default_api_key = ai_config.get('default_api_key')
        
        # 如果没有指定服务名称，使用默认服务
        if not service_name:
            service_name = ai_config.get('default')
            if not service_name:
                raise Exception("未配置默认AI服务")
        
        # 获取服务配置
        service_config = ai_config.get(service_name)
        if not service_config:
            raise Exception(f"未找到AI服务配置: {service_name}")
        
        # 如果服务没有配置api_key，使用默认api_key
        if 'api_key' not in service_config and default_api_key:
            service_config['api_key'] = default_api_key
        
        # 验证必要的配置项
        required_fields = {
            'oneapi': ['api_key', 'api_base', 'model'],
            'openai': ['api_key', 'api_base', 'model'],
            'gemini': ['api_key'],
            'azure': ['api_key', 'api_base'],
            'xunfei': ['app_id', 'api_key', 'api_secret']
        }
        
        # 检查必要的配置项
        if service_name in required_fields:
            missing_fields = [
                field for field in required_fields[service_name]
                if not service_config.get(field)
            ]
            if missing_fields:
                raise Exception(
                    f"AI服务 {service_name} 缺少必要的配置项: {', '.join(missing_fields)}"
                )
        
        # 返回完整的配置
        return {
            'name': service_config.get('name', service_name.title()),
            'service': service_name,
            **service_config
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self._config.get('logging', {'level': 'info'})
    
    def get_security_config(self) -> Dict[str, Any]:
        """获取安全配置"""
        return self._config.get('security', {})
    
    def get_redis_config(self) -> Dict[str, Any]:
        """获取Redis配置"""
        return self._config.get('redis', {})
    
    def get_rate_limit_config(self) -> Dict[str, Any]:
        """获取限流配置"""
        return self._config.get('rate_limit', {}) 