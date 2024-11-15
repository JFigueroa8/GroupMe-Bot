import requests

def snoop_who(access_token, bot_id, groupme_url):
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
        "url": "https://i.groupme.com/480x270.gif.5dbc45a946f84ca586d8995d549e9c9b"
      }
    ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)