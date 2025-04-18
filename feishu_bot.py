import datetime
import json
import traceback
import requests
import os
from dotenv import load_dotenv
import schedule
import time

load_dotenv()


def push_news():

    try_times = 0
    while try_times < 5:
        try:
            webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
            today = datetime.datetime.now().astimezone().strftime("%Y-%m-%d")
            data = requests.get(
                f"https://www.aicpb.com/api/dailyReports/get?date={today}"
            )
            data = data.json()

            news = ""
            for i, item in enumerate(data["data"]["news"]):
                news += f"[{i}. {item['title']}](https://chat.baidu.com/search?word={item['title']})\n"

            headers = {
                "Content-Type": "application/json; charset=utf-8",
            }
            payload_message = {
                "msg_type": "text",
                "content": {
                    "text": news
                    + "\n"
                    # @ 所有人 <at user_id="all">所有人</at>
                    # "text": content + "<at user_id=\"all\">test</at>"
                },
            }
            response = requests.post(
                url=webhook_url, data=json.dumps(payload_message), headers=headers
            )
            print(response.json())

            if response.status_code == 200:
                return  # 成功则直接返回

        except Exception as e:
            traceback.print_exc()
            try_times += 1
            time.sleep(10 * 60)  # 10分钟重试一次


if __name__ == "__main__":

    # 执行发送文本消息
    schedule.every().day.at("20:00").do(push_news)

    while True:
        schedule.run_pending()
        time.sleep(1)
