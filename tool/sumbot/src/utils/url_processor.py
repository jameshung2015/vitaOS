import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
import aiofiles
from datetime import datetime
import os

class URLProcessor:
    def __init__(self):
        self.history_dir = "output/urlhistory"
        os.makedirs(self.history_dir, exist_ok=True)

    async def record_url_history(self, url: str, tags: list = None) -> None:
        """
        记录URL处理历史
        """
        current_date = datetime.now().strftime("%Y%m%d")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_file = os.path.join(self.history_dir, f"{current_date}.md")
        
        # 准备记录内容
        tags_str = " ".join([f"#{tag}" for tag in (tags or [])])
        record = f"\n- {url} | {current_time} | {tags_str}"
        
        # 写入历史记录
        async with aiofiles.open(history_file, mode='a', encoding='utf-8') as f:
            await f.write(record)

    async def get_url_content(self, url: str, tags: list = None) -> str:
        """
        获取URL内容并记录历史
        """
        try:
            # 记录URL历史
            await self.record_url_history(url, tags)
            
            async with aiohttp.ClientSession() as session:
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                    async with session.get(url, headers=headers) as response:
                        if response.status != 200:
                            raise HTTPException(
                                status_code=400,
                                detail=f"无法访问 URL: HTTP {response.status}"
                            )
                        
                        content = await response.text()
                        
                        # 解析 HTML 内容
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        # 处理微信公众号文章
                        if 'mp.weixin.qq.com' in url:
                            return await self._process_wechat_article(soup)
                        else:
                            # 处理其他网页
                            return await self._process_general_webpage(soup)
                except Exception as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"处理 URL 时出错: {str(e)}"
                    )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"记录 URL 历史时出错: {str(e)}"
            )

    async def _process_wechat_article(self, soup: BeautifulSoup) -> str:
        """
        处理微信公众号文章
        """
        article_content = []
        
        # 获取标题（尝试多个可能的选择器）
        title = (
            soup.find('h1', class_='rich_media_title') or
            soup.find('h1', id='activity-name') or
            soup.find('h1')
        )
        if title:
            article_content.append(f"标题：{title.get_text().strip()}")
        
        # 获取作者信息（尝试多个可能的选择器）
        author = (
            soup.find('a', class_='rich_media_meta rich_media_meta_link rich_media_meta_nickname') or
            soup.find('span', class_='rich_media_meta_text') or
            soup.find('a', id='js_name')
        )
        if author:
            article_content.append(f"作者：{author.get_text().strip()}")
        
        # 获取文章内容（尝试多个可能的选择器）
        article = (
            soup.find('div', class_='rich_media_content') or
            soup.find('div', id='js_content') or
            soup.find('div', class_='content')
        )
        
        if article:
            # 移除所有脚本和样式
            for element in article(['script', 'style']):
                element.decompose()
            
            # 获取所有文本内容
            paragraphs = article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section'])
            for p in paragraphs:
                text = p.get_text().strip()
                if text:  # 只添加非空文本
                    article_content.append(text)
            
            # 如果没有找到段落，尝试直接获取文本
            if not paragraphs:
                text = article.get_text().strip()
                if text:
                    article_content.append(text)
        
        if not article_content:
            # 如果仍然没有内容，尝试获取页面上的所有文本
            texts = soup.stripped_strings
            article_content = [text.strip() for text in texts if text.strip()]
        
        if not article_content:
            raise HTTPException(
                status_code=400,
                detail="无法提取文章内容"
            )
        
        return "\n".join(article_content)

    async def _process_general_webpage(self, soup: BeautifulSoup) -> str:
        """
        处理一般网页
        """
        # 移除脚本和样式
        for script in soup(['script', 'style']):
            script.decompose()
        
        # 获取标题
        title = soup.find('title')
        content = []
        if title:
            content.append(f"标题：{title.get_text().strip()}")
        
        # 获取主要内容
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if main_content:
            # 获取所有段落文本
            paragraphs = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            for p in paragraphs:
                text = p.get_text().strip()
                if text:  # 只添加非空文本
                    content.append(text)
        
        if not content:
            # 如果没有找到主要内容，则获取所有文本
            content = [text.strip() for text in soup.stripped_strings]
        
        return "\n".join(content) 