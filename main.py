import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

GROUP_NAME = os.getenv("GROUP_NAME")
BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
GIPHY_KEY = os.getenv("GIPHY_KEY")

url = f"https://api.groupme.com/v3/bots/post?bot_id={BOT_ID}"

payload = json.dumps({"text": "Heroku test"})

x = requests.post(url, data=payload)

print(x.text)
