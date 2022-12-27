from config import access_token, bot_id, group_id
import datetime
import time
import requests

# Replace YOUR_ACCESS_TOKEN with your actual GroupMe API access token
# Replace YOUR_GROUP_ID with the ID of the GroupMe group you want to send the message to
ACCESS_TOKEN = access_token
GROUP_ID = group_id
groupme_url = 'https://api.groupme.com/v3/bots/post'
zenquotes_url = 'https://zenquotes.io/api/random'

# Set the time you want the message to be sent every day (in EST)
SEND_TIME = "09:00:00"

def send_message():
  # The message you want to send
  zenquotes_data = requests.get(zenquotes_url).json()
  quote = zenquotes_data[0]['q']
  author = zenquotes_data[0]['a']

  payload = {
        'bot_id': bot_id,
        'text': f'"{quote}" - {author}',
      }
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }
  response = requests.post(groupme_url, json=payload, headers=headers)

# Schedule the send_message function to run every day at SEND_TIME
while True:
  # Get the current time
  current_time = datetime.datetime.now().strftime("%H:%M:%S")

  # If the current time is equal to the send time, run the send_message function
  if current_time == SEND_TIME:
    send_message()

  # Sleep for one hour before checking the time again
  time.sleep(3600)
