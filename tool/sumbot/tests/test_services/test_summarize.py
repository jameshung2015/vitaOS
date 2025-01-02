import pytest
from src.services.summarize import SummarizeService

class TestSummarizeService:
    @pytest.mark.asyncio
    async def test_summarize_url_wechat(self, summarize_service):
        """
        测试微信文章URL总结功能
        """
        # 测试URL
        url = "https://mp.weixin.qq.com/s/xQn9K7lzJ0L2aiii03ERXA"
        
        # 执行总结
        summary = await summarize_service.summarize_url(url)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # 验证总结内容的基本结构
        lines = summary.split('\n')
        assert len(lines) >= 2  # 至少包含主旨和要点
        
        # 验证是否包含关键词
        assert any('Cursor' in line for line in lines)

    @pytest.mark.asyncio
    async def test_summarize_url_invalid(self, summarize_service):
        """
        测试无效URL的处理
        """
        # 测试无效URL
        url = "https://invalid-url.com/article"
        
        # 验证是否抛出异常
        with pytest.raises(Exception) as exc_info:
            await summarize_service.summarize_url(url)
        
        # 验证错误信息
        assert "无法访问URL" in str(exc_info.value) or "处理URL时出错" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_summarize_url_non_wechat(self, summarize_service):
        """
        测试非微信文章URL的处理
        """
        # 测试普通网页URL（使用一个稳定的测试页面）
        url = "https://example.com"
        
        # 执行总结
        summary = await summarize_service.summarize_url(url)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
``` 