import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROUP_NAME = os.getenv("GROUP_NAME")
BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
GIPHY_KEY = os.getenv("GIPHY_KEY")


