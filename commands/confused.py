import requests

def confused(access_token, bot_id, groupme_url):
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
              "url": "https://i.groupme.com/268x274.gif.ff4ccbc619bc472db0ef8d25e3798566"
          }
      ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
