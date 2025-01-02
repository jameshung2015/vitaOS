import re
from fastapi import HTTPException
from typing import Optional

class APIKeyValidator:
    """API密钥验证器"""
    
    # API密钥格式：sk-开头，后跟40-50个字符
    KEY_PATTERN = re.compile(r'^sk-[A-Za-z0-9]{40,50}$')
    
    @classmethod
    def is_valid(cls, api_key: Optional[str]) -> bool:
        """
        验证API密钥是否有效
        :param api_key: API密钥
        :return: 是否有效
        """
        if not api_key:
            return False
        
        return cls.check_format(api_key) and cls.check_security(api_key)
    
    @classmethod
    def check_format(cls, api_key: str) -> bool:
        """
        检查API密钥格式
        :param api_key: API密钥
        :return: 格式是否正确
        """
        return bool(cls.KEY_PATTERN.match(api_key))
    
    @classmethod
    def check_security(cls, api_key: str) -> bool:
        """
        检查API密钥安全性
        :param api_key: API密钥
        :return: 是否满足安全要求
        """
        if not api_key.startswith('sk-'):
            return False
        
        # 移除前缀后的实际密钥部分
        key = api_key[3:]
        
        # 检查长度（不包括前缀）
        if len(key) < 40 or len(key) > 50:
            return False
        
        # 检查复杂度
        has_upper = any(c.isupper() for c in key)
        has_lower = any(c.islower() for c in key)
        has_digit = any(c.isdigit() for c in key)
        
        # 必须同时包含大写字母、小写字母和数字
        return has_upper and has_lower and has_digit

async def validate_api_key(api_key: Optional[str]) -> None:
    """
    验证API密钥，无效则抛出异常
    :param api_key: API密钥
    :raises: HTTPException 如果API密钥无效
    """
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="缺少API密钥"
        )
    
    if not APIKeyValidator.is_valid(api_key):
        raise HTTPException(
            status_code=401,
            detail="无效的API密钥"
        ) 