# fastapi
import datetime
from fastapi import FastAPI
import asyncio
import httpx
import uvicorn

app = FastAPI()


@app.get("/news")
async def root():
    async with httpx.AsyncClient() as client:

        # 获取当前日期()
        # today = datetime.datetime.now(tz="").strftime("%Y-%m-%d")
        # 获取当前时区的日期
        today = datetime.datetime.now().astimezone().strftime("%Y-%m-%d")

        response = await client.get(
            f"https://www.aicpb.com/api/dailyReports/get?date={today}"
        )
        return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
