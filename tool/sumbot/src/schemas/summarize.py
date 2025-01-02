from pydantic import BaseModel, HttpUrl
from typing import Optional, List

class URLSummarizeRequest(BaseModel):
    url: HttpUrl
    api_key: Optional[str] = None
    tags: Optional[List[str]] = None
    max_length: Optional[int] = 500

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "api_key": "sk-your-api-key",
                "tags": ["技术", "AI"],
                "max_length": 500
            }
        }

class URLSummarizeResponse(BaseModel):
    summary: str
    source_url: Optional[HttpUrl] = None
    
class SearchSummarizeRequest(BaseModel):
    query: str
    max_results: Optional[int] = 5
    
class SearchSummarizeResponse(BaseModel):
    summary: str
    sources: Optional[List[str]] = None

class ImageAnalysisResponse(BaseModel):
    description: str
    tags: Optional[List[str]] = None
    
class VideoSummarizeResponse(BaseModel):
    title: Optional[str] = None
    summary: str
    duration: Optional[str] = None
    platform: Optional[str] = None

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    context_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    context_id: str 