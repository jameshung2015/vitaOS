import pytest
from src.utils.ai_service import AIService

class TestAIService:
    @pytest.mark.asyncio
    async def test_generate_summary(self, ai_service):
        """
        测试文本总结生成功能
        """
        # 测试文本
        test_content = """
        Cursor是一个强大的AI编程助手，它提供了多种功能来提升开发效率。
        主要功能包括代码补全、代码解释和重构建议等。
        通过@notepads功能，开发者可以快速记录和组织笔记。
        使用@web功能可以直接在编辑器中搜索和浏览网页内容。
        Bug finder功能帮助开发者快速定位和修复代码中的问题。
        """
        
        # 执行总结
        summary = await ai_service.generate_summary(test_content)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # 验证总结内容的基本结构
        lines = summary.split('\n')
        assert len(lines) >= 2  # 至少包含主旨和要点
        
        # 验证是否包含关键词
        assert 'Cursor' in summary
        assert any('功能' in line for line in lines)

    @pytest.mark.asyncio
    async def test_generate_summary_empty_content(self, ai_service):
        """
        测试空内容的处理
        """
        # 测试空内容
        test_content = ""
        
        # 执行总结并验证结果
        summary = await ai_service.generate_summary(test_content)
        assert summary is not None
        assert isinstance(summary, str)

    @pytest.mark.asyncio
    async def test_generate_summary_long_content(self, ai_service):
        """
        测试长文本的处理
        """
        # 生成长文本
        test_content = "这是一个测试句子。\n" * 100
        
        # 执行总结
        summary = await ai_service.generate_summary(test_content)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) < len(test_content)  # 确保总结比原文短 