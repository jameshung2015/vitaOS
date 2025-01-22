# SumBot

文章总结和问答服务

## 功能特点

- 支持URL内容总结
- 支持文件内容总结
- 支持视频内容总结（B站、抖音、YouTube、小红书）
- 支持图片内容分析
- 支持搜索内容总结
- 自动生成追问问题
- 支持多种AI模型（OpenAI、OneAPI、Gemini、Azure、讯飞）
- 支持限流和缓存
- URL历史记录（按日期自动保存）
- 支持内容标签管理

## 快速开始

1. 克隆项目
```bash
# 克隆代码仓库并进入项目目录
git clone https://github.com/yourusername/sumbot.git
cd sumbot
```

2. 安装依赖
```bash
# 安装项目所需的Python包
pip install -r requirements.txt
```

3. 配置服务
```bash
# 创建配置文件
cp config.json.template config.json
```

编辑 `config.json` 文件，设置必要的配置项：
```json
# 完整配置文件示例
{
    "api": {
        "version": "v1",
        "prefix": "/api/v1",
        "name": "SumBot",
        "host": "0.0.0.0",
        "port": 5566,
        "reload": true
    },
    "ai_service": {
        "default": "oneapi",
        "oneapi": {
            "name": "OneAPI",
            "api_key": "your_api_key_here",
            "api_base": "your_api_base_url_here",
            "model": "your_model_name_here"
        },
        "openai": {
            "name": "OpenAI",
            "api_key": "your_api_key_here",
            "api_base": "your_api_base_url_here",
            "model": "your_model_name_here"
        },
        "gemini": {
            "name": "Google Gemini",
            "api_key": null
        },
        "azure": {
            "name": "Azure OpenAI",
            "api_key": null,
            "api_base": null
        },
        "xunfei": {
            "name": "讯飞星火",
            "app_id": null,
            "api_key": null,
            "api_secret": null
        }
    },
    "logging": {
        "level": "info"
    }
}
```

4. 启动服务
```bash
# 启动SumBot服务
python3 run.py
```

## 服务管理

### 启动服务
```bash
# 启动服务（默认在5566端口）
python3 run.py

# 常驻服务 
nohup python3 run.py &
```

### 重启服务
```bash
# 重启服务（会先停止当前运行的实例）
python3 run.py restart
```

### 停止服务
```bash
# 停止当前运行的服务实例
python3 run.py stop
```

### 查看服务状态
```bash
# 查看服务运行状态、进程信息和API可用性
python3 run.py status

# 查看 5566 port 的运行状态
netstat -tuln | grep 5566
(windows)netstat -ano | findstr 5566
```

### 设置服务配置
```bash
# 设置默认AI服务
python3 run.py set --service oneapi

# 设置服务的API密钥
python3 run.py set --service oneapi --api-key sk-your-api-key

# 设置默认API密钥（用于未配置密钥的服务）
python3 run.py set --api-key sk-your-default-key
```

## API 文档

启动服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:5566/docs
- ReDoc: http://localhost:5566/redoc

### API 密钥认证

为了保护API服务，所有请求都需要提供有效的API密钥。API密钥应通过HTTP请求头的`Authorization`字段提供，格式为`Bearer YOUR_API_KEY`。

### API密钥要求

- 长度：至少32个字符
- 格式：必须以`sk-`开头，后跟字母数字字符
- 安全性：不应包含任何敏感信息或个人标识信息

### 获取API密钥

1. 联系管理员申请API密钥
2. 收到密钥后，建议将其保存在环境变量中：
   ```bash
   # Linux/macOS
   export SUMBOT_API_KEY='your-api-key'
   
   # Windows (PowerShell)
   $env:SUMBOT_API_KEY='your-api-key'
   ```

### API密钥错误处理

当API密钥验证失败时，服务器将返回以下错误：

```json
{
    "detail": "无效的API密钥"
}
```

常见的API密钥错误：
- 401 Unauthorized: API密钥无效或未提供
- 403 Forbidden: API密钥已被禁用或超出使用限制

## 配置说明

### 配置文件结构

`config.json` 包含以下主要配置项：

```json
# 完整配置文件示例
{
    "api": {
        "version": "v1",
        "prefix": "/api/v1",
        "name": "SumBot",
        "host": "0.0.0.0",
        "port": 5566,
        "reload": true
    },
    "ai_service": {
        "default": "oneapi",
        "default_api_key": "your_default_api_key_here",  # 默认API密钥，用于未配置密钥的服务
        "oneapi": {
            "name": "OneAPI",
            "api_key": "your_api_key_here",
            "api_base": "your_api_base_url_here",
            "model": "your_model_name_here"
        },
        "openai": {
            "name": "OpenAI",
            "api_key": "your_api_key_here",
            "api_base": "your_api_base_url_here",
            "model": "your_model_name_here"
        },
        "gemini": {
            "name": "Google Gemini",
            "api_key": null
        },
        "azure": {
            "name": "Azure OpenAI",
            "api_key": null,
            "api_base": null
        },
        "xunfei": {
            "name": "讯飞星火",
            "app_id": null,
            "api_key": null,
            "api_secret": null
        }
    },
    "logging": {
        "level": "info"
    }
}
```

### 配置项说明

- `api`: API服务配置
  - `version`: API版本
  - `prefix`: API路由前缀
  - `name`: 服务名称
  - `host`: 服务主机地址
  - `port`: 服务端口
  - `reload`: 是否启用热重载

- `ai_service`: AI服务配置
  - `default`: 默认使用的AI服务（oneapi/openai/gemini/azure/xunfei）
  - `default_api_key`: 默认API密钥，当具体服务未配置api_key时使用
  - `oneapi`: OneAPI配置（优先使用）
    - `name`: 服务名称
    - `api_key`: API密钥
    - `api_base`: API基础URL
    - `model`: 使用的模型名称
  - `openai`: OpenAI配置
    - `name`: 服务名称
    - `api_key`: API密钥
    - `api_base`: API基础URL
    - `model`: 使用的模型名称
  - `gemini`: Google Gemini配置
    - `name`: 服务名称
    - `api_key`: API密钥
  - `azure`: Azure OpenAI配置
    - `name`: 服务名称
    - `api_key`: API密钥
    - `api_base`: API基础URL
  - `xunfei`: 讯飞星火配置
    - `name`: 服务名称
    - `app_id`: 应用ID
    - `api_key`: API密钥
    - `api_secret`: API密钥密文

### 动态配置管理

服务提供了命令行工具用于动态管理AI服务配置：

1. 切换默认服务：
   ```bash
   python3 run.py set --service oneapi
   ```

2. 更新服务API密钥：
   ```bash
   python3 run.py set --service oneapi --api-key sk-your-api-key
   ```

3. 设置默认API密钥：
   ```bash
   python3 run.py set --api-key sk-your-default-key
   ```

注意事项：
- API密钥必须以 `sk-` 开头
- 设置默认API密钥后，未配置密钥的服务将使用该默认密钥
- 服务名称必须是已在配置文件中定义的服务之一

- `logging`: 日志配置
  - `level`: 日志级别（支持 debug、info、warning、error）

## 使用示例

### 内容总结功能

设定环境 key
'$env:SUMBOT_API_KEY = "sk-your-api-key-here"'

#### URL内容总结

```python
# 使用Python requests库调用URL总结API的示例
import requests
import os

# 从环境变量获取API密钥
api_key = os.getenv('SUMBOT_API_KEY')
if not api_key:
    raise ValueError("请设置 SUMBOT_API_KEY 环境变量")

url = "http://localhost:5566/api/v1/summarize/url"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {
    "url": "https://example.com/article",  # 要总结的文章URL
    "tags": ["技术", "AI", "编程"],       # 可选，文章标签列表
    "max_length": 500                     # 可选，总结最大长度
}

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # 检查响应状态
    print(response.json())
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("API密钥验证失败")
    elif e.response.status_code == 422:
        print("请求参数验证失败")
    else:
        print(f"请求失败: {e}")
```

响应格式：
```json
# API响应JSON格式示例
{
    "summary": "文章总结内容",
    "source_url": "https://example.com/article"  # 原文URL
}
```

请求参数说明：
- `url`: 必填，要总结的文章URL（必须是有效的HTTP/HTTPS URL）
- `tags`: 可选，文章标签列表（用于分类和检索）
- `max_length`: 可选，总结最大长度，默认500字

请求头说明：
- `Content-Type`: 必填，值为 `application/json`
- `Authorization`: 必填，值为 `Bearer YOUR_API_KEY`

#### 文件内容总结

支持多种文件格式的内容总结，包括：
- 文本文件（.txt, .md）
- PDF文档
- Word文档
- 代码文件

请求示例：
```python
import requests

url = "http://localhost:5566/api/v1/summarize/file"
headers = {
    "Authorization": f"Bearer {api_key}"
}
files = {
    'file': open('example.pdf', 'rb')
}

response = requests.post(url, files=files, headers=headers)
print(response.json())
```

#### 视频内容总结

支持以下平台的视频内容总结：
- B站
- 抖音
- YouTube
- 小红书

请求示例：
```python
import requests

url = "http://localhost:5566/api/v1/summarize/video"
headers = {
    "Authorization": f"Bearer {api_key}"
}
data = {
    "url": "https://www.bilibili.com/video/BV1xx411c7mD"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

#### 图片内容分析

支持图片内容识别和分析，包括：
- 文字识别（OCR）
- 图像描述生成
- 图像分类

请求示例：
```python
import requests

url = "http://localhost:5566/api/v1/analyze/image"
headers = {
    "Authorization": f"Bearer {api_key}"
}
files = {
    'file': open('example.jpg', 'rb')
}

response = requests.post(url, files=files, headers=headers)
print(response.json())
```

#### 搜索内容总结

支持对搜索结果进行总结，包括：
- 网页搜索
- 学术论文搜索
- 新闻搜索

请求示例：
```python
import requests

url = "http://localhost:5566/api/v1/summarize/search"
headers = {
    "Authorization": f"Bearer {api_key}"
}
data = {
    "query": "人工智能最新进展",
    "max_results": 5
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### URL历史记录

系统会自动在 `output/urlhistory` 目录下按日期（YYYYMMDD.md）记录所有处理过的URL，包含以下信息：
- URL地址
- 处理时间
- 标签信息

示例记录格式：
```markdown
# URL历史记录示例（保存在YYYYMMDD.md文件中）
- https://example.com/article | 2024-12-31 15:30:45 | #技术 #AI #编程
