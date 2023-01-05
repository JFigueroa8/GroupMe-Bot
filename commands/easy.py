import requests

def its_easy_boys(access_token, bot_id, groupme_url):
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
        "preview_url": "https://v.groupme.com/88126238/2023-01-01T02:09:53Z/745877f1.1080x1920r0.jpg",
        "url": "https://v.groupme.com/88126238/2023-01-01T02:09:53Z/745877f1.1080x1920r0.mp4"
      }
    ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)