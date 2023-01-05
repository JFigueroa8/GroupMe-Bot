import requests

def fart(access_token, bot_id, groupme_url):
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
              "preview_url": "https://v.groupme.com/88126238/2023-01-01T18:21:09Z/34b5566a.1280x720r0.jpg",
              "url": "https://v.groupme.com/88126238/2023-01-01T18:21:09Z/34b5566a.1280x720r0.mp4"
          }
      ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
