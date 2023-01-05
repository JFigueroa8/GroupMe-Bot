import requests

def clutch(access_token, bot_id, groupme_url):
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
        "preview_url": "https://v.groupme.com/88126238/2022-12-30T18:32:32Z/408d8300.1920x1080r0.jpg",
        "url": "https://v.groupme.com/88126238/2022-12-30T18:32:32Z/408d8300.1920x1080r0.mp4"
      }
    ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)