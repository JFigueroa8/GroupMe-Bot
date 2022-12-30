import requests
from config import access_token, bot_id
from urls import groupme_url

def allen_dance():
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'attachments': [
      {
        "type":"image",
        "url":"https://i.groupme.com/330x200.gif.9de6ba82c66a4a7c86b4f6be307b731e"
      }
    ],
  }
  response = requests.post(groupme_url, json=payload, headers=headers)