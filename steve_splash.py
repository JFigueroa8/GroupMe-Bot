import requests
from config import access_token, bot_id
from urls import groupme_url

def splash():
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
        "url": "https://i.groupme.com/720x479.gif.889e4a2ff89f491aae8fdfb37a1f151e"
      }
    ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)