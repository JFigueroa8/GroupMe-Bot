import requests

def cam(access_token, bot_id, groupme_url):
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
              "url": "https://i.groupme.com/478x262.gif.8d7ffad57d994479b50b6dc334aad423"
          }
      ],
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
