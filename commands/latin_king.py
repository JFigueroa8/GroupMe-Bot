import requests
import random

def latin_king(access_token, bot_id, groupme_url):
  gifs = [
      {
          "type": "image",
          "url": "https://i.groupme.com/498x363.gif.f9eac30754d34231ba419de2ae762f27"
      },
      {
          "type": "image",
          "url": "https://i.groupme.com/498x280.gif.9d642dcb9d6649cfb202421f203bf923"
      }
  ]

  selected_gif = random.choice(gifs)

  # Set the headers and payload
  headers = {
      'Content-Type': 'application/json',
      'X-Access-Token': access_token,
  }

  payload = {
      'bot_id': bot_id,
      'attachments': [
          selected_gif
      ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
