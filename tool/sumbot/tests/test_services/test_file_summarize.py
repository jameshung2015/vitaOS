import pytest
import os
from pathlib import Path
from fastapi import UploadFile
from src.services.summarize import SummarizeService

class TestFileSummarize:
    @pytest.fixture
    def test_data_dir(self):
        """
        提供测试数据目录路径
        """
        return Path(__file__).parent.parent / "test-data"

    async def _create_upload_file(self, file_path: Path):
        """
        创建 UploadFile 对象
        """
        with open(file_path, 'rb') as f:
            content = f.read()
        
        return UploadFile(
            filename=file_path.name,
            file=None,
            content=content
        )

    @pytest.mark.asyncio
    async def test_summarize_txt_file(self, summarize_service, test_data_dir):
        """
        测试文本文件总结
        """
        # 准备测试文件
        file_path = test_data_dir / "sample.txt"
        upload_file = await self._create_upload_file(file_path)
        
        # 执行总结
        summary = await summarize_service.summarize_file(upload_file)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # 验证总结内容
        assert "文件内容总结" in summary or "测试文档" in summary

    @pytest.mark.asyncio
    async def test_summarize_markdown_file(self, summarize_service, test_data_dir):
        """
        测试 Markdown 文件总结
        """
        # 准备测试文件
        file_path = test_data_dir / "sample.md"
        upload_file = await self._create_upload_file(file_path)
        
        # 执行总结
        summary = await summarize_service.summarize_file(upload_file)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # 验证总结内容
        assert "Markdown" in summary or "测试文档" in summary

    @pytest.mark.asyncio
    async def test_summarize_invalid_file(self, summarize_service):
        """
        测试无效文件处理
        """
        # 创建无效文件
        upload_file = UploadFile(
            filename="test.invalid",
            file=None,
            content=b"Invalid file content"
        )
        
        # 验证是否抛出异常
        with pytest.raises(Exception) as exc_info:
            await summarize_service.summarize_file(upload_file)
        
        # 验证错误信息
        assert "不支持的文件类型" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_summarize_empty_file(self, summarize_service):
        """
        测试空文件处理
        """
        # 创建空文件
        upload_file = UploadFile(
            filename="empty.txt",
            file=None,
            content=b""
        )
        
        # 执行总结
        summary = await summarize_service.summarize_file(upload_file)
        
        # 验证总结结果
        assert summary is not None
        assert isinstance(summary, str)
``` 