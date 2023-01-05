import requests
import random

def spider_monkey(access_token, bot_id, groupme_url):
  videos = [
      {
          "type": "video",
          "preview_url": "https://v.groupme.com/88126238/2023-01-01T16:59:53Z/7195a299.640x480r0.jpg",
          "url": "https://v.groupme.com/88126238/2023-01-01T16:59:53Z/7195a299.640x480r0.mp4"
      },
      {
          "type": "video",
          "preview_url": "https://v.groupme.com/88126238/2023-01-01T17:00:32Z/1b2ff431.640x480r0.jpg",
          "url": "https://v.groupme.com/88126238/2023-01-01T17:00:32Z/1b2ff431.640x480r0.mp4"
      },
      {
          "type": "video",
          "preview_url": "https://v.groupme.com/88126238/2023-01-01T17:00:54Z/21c15ccc.640x480r0.jpg",
          "url": "https://v.groupme.com/88126238/2023-01-01T17:00:54Z/21c15ccc.640x480r0.mp4"
      }
  ]

  selected_video = random.choice(videos)

  # Set the headers and payload
  headers = {
      'Content-Type': 'application/json',
      'X-Access-Token': access_token,
  }

  payload = {
      'bot_id': bot_id,
      'attachments': [
          selected_video
      ],
  }

  # Send the video to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
