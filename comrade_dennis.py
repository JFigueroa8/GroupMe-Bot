import requests
from config import access_token, bot_id
from urls import groupme_url


def comrade_dennis():
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
              "url": "https://i.groupme.com/918x750.jpeg.276d75afaefa4bfb9544ef8c7042ff96"
          }
      ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
