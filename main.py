import asyncio
import os
import re
from crawl4ai import *

from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


# print(os.getenv("SILICON_API_KEY"))
client = OpenAI(
    api_key=os.getenv("SILICON_API_KEY"), base_url="https://api.siliconflow.cn/v1"
)


async def main():
    async with AsyncWebCrawler() as crawler:
        result: CrawlResult = await crawler.arun(
            # url="https://www.nbcnews.com/business",
            # url="https://www.aicpb.com/news"
            url="https://www.36kr.com/p/3253687914983172"
        )

        m = str(result.markdown)
        pattern = r"!\[.*?\]\(.*?\)|(\[.*?\]\(.*?\))"
        article = m[
            m.find("# ") : m.find(
                "该文观点仅代表作者本人，36氪平台仅提供信息存储空间服务。"
            )
        ]
        article = article[article.find("\n"): ]
        cleaned_text = re.sub(pattern, "", article)
        print(cleaned_text)

        response = client.chat.completions.create(
            # model='Pro/deepseek-ai/DeepSeek-R1',
            model="Qwen/Qwen2.5-72B-Instruct",
            temperature=0.6,
            messages=[
                {
                    "role": "user",
                    # "content": "你是新闻专家，请你为下面文章的起一个标题,标题要精简并且能概况核心内容, 不需要给出任何解释:   \n\n======"
                    "content": "你是新闻专家，请你简短地概况下面这片文章的核心内容, 不需要给出任何解释:   \n\n======"
                    + cleaned_text
                    + "=====",
                }
            ],
            stream=True,
        )
        print("===========================")
        # print(response.response.)
        for chunk in response:
            if not chunk.choices:
                continue
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
            if chunk.choices[0].delta.reasoning_content:
                print(chunk.choices[0].delta.reasoning_content, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
    # re_test()
