import requests
import random

def grow_up(access_token, bot_id, groupme_url):
  gifs = [
      {
          'type': 'image',
          'url': 'https://i.groupme.com/480x271.gif.e4c13f006ca44e0695b2257bc7c2c53a'
      },
      {
          'type': 'image',
          'url': 'https://i.groupme.com/480x266.gif.3951108fc58e416496239e6dce0dc52e'
      },
      {
          'type': 'image',
          'url': 'https://i.groupme.com/498x278.gif.e3b60eedc7f44521b5ebad1fe05ea9b3'
      },
      {
          'type': 'image',
          'url': 'https://i.groupme.com/407x480.gif.415d8b6f0a1a4a939fcf6fe7c32901ec'
      },
      {
          'type': 'image',
          'url': 'https://i.groupme.com/392x480.gif.2e57207ce05d4ef5ad90f1d8eb9051cd'
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
