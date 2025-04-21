stop:
	ps aux | grep 'python feishu_bot.py' | grep -v grep | awk '{print $$2}' | xargs kill
start:
	nohup .venv/bin/python feishu_bot.py > bot.log 2>&1 &