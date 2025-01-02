import requests

def test_file_upload():
    url = "http://localhost:8000/api/v1/summarize/file"
    
    # 打开测试文件
    files = {
        'file': ('sample.txt', open('tests/test-data/sample.txt', 'rb'), 'text/plain')
    }
    
    try:
        # 发送请求
        response = requests.post(url, files=files)
        
        # 打印响应
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        # 关闭文件
        files['file'][1].close()

if __name__ == "__main__":
    test_file_upload() 