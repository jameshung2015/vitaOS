import pytest
from src.utils.config_manager import ConfigManager
from src.utils.ai_service import AIService
from run import set_ai_service

def test_set_ai_service():
    """测试设置AI服务配置"""
    # 测试设置默认服务
    result = set_ai_service(service_name="oneapi")
    assert result is True
    
    config = ConfigManager()
    ai_config = config.get_ai_service_config()
    assert ai_config['service'] == "oneapi"
    
    # 测试设置API密钥
    test_key = "sk-test-key-123456"
    result = set_ai_service(service_name="oneapi", api_key=test_key)
    assert result is True
    
    ai_config = config.get_ai_service_config("oneapi")
    assert ai_config['api_key'] == test_key

def test_set_ai_service_invalid_input():
    """测试无效输入"""
    # 测试无效的服务名称
    result = set_ai_service(service_name="invalid_service")
    assert result is False
    
    # 测试无效的API密钥格式
    result = set_ai_service(service_name="oneapi", api_key="invalid-key")
    assert result is False

def test_default_api_key():
    """测试默认API密钥"""
    config = ConfigManager()
    
    # 设置默认API密钥
    result = set_ai_service(api_key="sk-default-test-key")
    assert result is True
    
    # 验证未配置API密钥的服务会使用默认密钥
    ai_config = config.get_ai_service_config("openai")
    assert ai_config['api_key'] == "sk-default-test-key"

@pytest.mark.asyncio
async def test_ai_service_with_custom_key():
    """测试使用自定义API密钥"""
    service = AIService()
    test_content = "这是一个测试内容。"
    custom_key = "sk-custom-test-key-123"
    
    try:
        # 使用自定义API密钥生成总结
        summary = await service.generate_summary(test_content, api_key=custom_key)
        assert summary is not None
        assert isinstance(summary, str)
    except Exception as e:
        assert "API密钥无效" in str(e)

@pytest.mark.asyncio
async def test_ai_service_with_default_key():
    """测试使用默认API密钥"""
    service = AIService()
    test_content = "这是一个测试内容。"
    
    try:
        # 使用默认API密钥生成总结
        summary = await service.generate_summary(test_content)
        assert summary is not None
        assert isinstance(summary, str)
    except Exception as e:
        assert "未提供API密钥" not in str(e) 