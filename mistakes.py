import requests
from config import access_token, bot_id
from urls import groupme_url


def mistakes():
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
              "url": "https://i.groupme.com/432x960.jpeg.c07a92abefa54098906210608994a561"
          }
      ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
