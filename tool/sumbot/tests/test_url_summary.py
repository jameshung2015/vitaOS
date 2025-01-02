import aiohttp
import asyncio
import json
import pytest
import os
from datetime import datetime

@pytest.mark.asyncio
async def test_url_summary():
    """
    测试URL总结功能
    """
    # 测试URL和标签
    test_url = "https://example.com"
    test_tags = ["测试", "示例", "自动化测试"]
    
    # API端点
    api_url = "http://localhost:5566/api/v1/summarize/url"
    
    print("\n开始测试URL总结功能...")
    print(f"目标URL: {test_url}")
    print(f"标签: {test_tags}")
    print("-" * 50)
    
    try:
        async with aiohttp.ClientSession() as session:
            # 准备请求数据
            data = {
                "url": test_url,
                "tags": test_tags
            }
            
            # 发送POST请求
            async with session.post(api_url, json=data) as response:
                print(f"状态码: {response.status}")
                
                # 获取响应内容
                result = await response.text()
                print("\n响应内容:")
                print("-" * 50)
                print(json.dumps(json.loads(result), ensure_ascii=False, indent=2))
                print("-" * 50)
                
                # 验证响应状态
                assert response.status == 200, f"请求失败: {response.status}"
                
                # 验证响应内容
                response_data = json.loads(result)
                assert "summary" in response_data, "响应中缺少summary字段"
                assert isinstance(response_data["summary"], str), "summary不是字符串类型"
                assert len(response_data["summary"]) > 0, "summary为空"
                
                # 验证历史记录文件
                current_date = datetime.now().strftime("%Y%m%d")
                history_file = os.path.join("output/urlhistory", f"{current_date}.md")
                
                print("\n验证历史记录文件...")
                assert os.path.exists(history_file), f"历史记录文件不存在: {history_file}"
                
                with open(history_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print("\n历史记录内容:")
                    print("-" * 50)
                    print(content)
                    print("-" * 50)
                    
                    # 验证URL是否记录
                    assert test_url in content, "URL未记录在历史文件中"
                    # 验证标签是否记录
                    for tag in test_tags:
                        assert f"#{tag}" in content, f"标签 #{tag} 未记录在历史文件中"
                
                print("\n测试通过！✓")
                
    except Exception as e:
        print("\n测试失败:")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(test_url_summary())
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        exit(1) 