# SumBot API 文档

## 简介

SumBot API 是一个内容总结服务，支持对 URL 内容和文件内容进行智能总结。

## API 端点

### 1. URL 内容总结

**端点：** `/api/v1/summarize/url`

**方法：** POST

**请求体：**
```json
{
    "url": "https://example.com/article"
}
```

**响应：**
```json
{
    "summary": "文章内容总结",
    "follow_up_questions": [
        "追问问题1",
        "追问问题2",
        "追问问题3"
    ]
}
```

**示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/summarize/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article"}'
```

### 2. 文件内容总结

**端点：** `/api/v1/summarize/file`

**方法：** POST

**请求：**
- 使用 multipart/form-data 格式
- 文件字段名：file

**支持的文件类型：**
- 文本文件 (.txt)
- Markdown 文件 (.md)
- PDF 文件 (.pdf)
- Word 文档 (.docx)
- Excel 文件 (.xlsx, .xls)
- PowerPoint 文件 (.pptx)

**响应：**
```json
{
    "summary": "文件内容总结",
    "follow_up_questions": [
        "追问问题1",
        "追问问题2",
        "追问问题3"
    ]
}
```

**示例：**
```bash
curl -X POST "http://localhost:8000/api/v1/summarize/file" \
     -F "file=@path/to/document.pdf"
```

## 错误处理

API 使用标准的 HTTP 状态码表示请求的结果：

- 200：请求成功
- 400：请求参数错误
- 500：服务器内部错误

错误响应格式：
```json
{
    "detail": "错误信息描述"
}
```

## 部署说明

1. 配置环境变量：
   - 复制 `.env.template` 为 `.env`
   - 填写必要的配置信息

2. 使用 Docker 部署：
```bash
# 构建镜像
docker build -t sumbot .

# 运行容器
docker run -d -p 8000:8000 \
    --env-file .env \
    sumbot
```

## API 文档

- Swagger UI：访问 `/docs`
- ReDoc：访问 `/redoc` 