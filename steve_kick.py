import requests
from config import access_token, bot_id
from urls import groupme_url

def kick():
  # Set the headers and payload
  headers = {
  'Content-Type': 'application/json',
  'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'attachments': [
      {
        "type": "video",
        "preview_url": "https://v.groupme.com/88126238/2022-12-30T18:46:12Z/7e34c71f.640x352r0.jpg",
        "url": "https://v.groupme.com/88126238/2022-12-30T18:46:12Z/7e34c71f.640x352r0.mp4"
      }
    ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)