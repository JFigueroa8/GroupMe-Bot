import requests
from config import access_token, bot_id
from urls import groupme_url


def middle_aged():
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
              "url": "https://i.groupme.com/444x419.jpeg.fea1a8e402194588b311254bf6769ab8"
          }
      ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
