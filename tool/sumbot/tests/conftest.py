import pytest
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# 导入项目模块
from src.services.summarize import SummarizeService
from src.utils.ai_service import AIService

@pytest.fixture
def summarize_service():
    """
    提供 SummarizeService 实例
    """
    return SummarizeService()

@pytest.fixture
def ai_service():
    """
    提供 AIService 实例
    """
    return AIService() 