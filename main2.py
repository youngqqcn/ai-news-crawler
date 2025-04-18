
import asyncio
import httpx





async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.aicpb.com/api/dailyReports/get?date=2025-01-27")
        # print(response.text)
        print(response.json())
        # print(response.status_code)
        # print(response.headers)
        # print(response.cookies)
        # print(response.history)
        # print(response.url)


    pass




if __name__ == "__main__":
    asyncio.run(main())