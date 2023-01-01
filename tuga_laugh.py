import requests
from config import access_token, bot_id
from urls import groupme_url

def tuga_laugh():
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
        "url": "https://i.groupme.com/440x464.gif.d1d896e3016e4a699e80a39f6778059f"
      }
    ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)