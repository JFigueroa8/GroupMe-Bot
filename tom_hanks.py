import requests
from config import access_token, bot_id
from urls import groupme_url

def busy():
  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'attachments': [
      {
        "type": "image",
        "url": "https://i.groupme.com/360x199.gif.df1deb23a93746bbbb4d33c0710a040c"
      }
    ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)