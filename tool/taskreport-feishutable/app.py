import requests

# 定义 URL 和 Bearer Token
url = ""  # 请填写你的 Webhook URL
bearer_token = ""  # 请填写你的 Bearer Token

# 设置请求头
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# 定义测试的 JSON payload
payload = {
    "task": "report work status"
}

# 发送 POST 请求
response = requests.post(url, headers=headers, json=payload)

# 检查响应状态码
if response.status_code == 200:
    try:
        print("请求成功")
        print("响应内容:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")
        print("响应内容:", response.text)
else:
    print(f"请求失败，状态码: {response.status_code}")
    print("响应内容:", response.text)