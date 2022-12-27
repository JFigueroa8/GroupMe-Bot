from config import access_token, bot_id, group_id
import datetime
import time
import requests

# Replace YOUR_ACCESS_TOKEN with your actual GroupMe API access token
# Replace YOUR_GROUP_ID with the ID of the GroupMe group you want to send the message to
ACCESS_TOKEN = access_token
GROUP_ID = group_id
zenquotes_url = 'https://zenquotes.io/api/random'

# Set the time you want the message to be sent every day (in EST)
SEND_TIME = "9:00"

def send_message():
  # The message you want to send
  message = "Hello, world!"
  zenquotes_data = requests.get(zenquotes_url).json()
  quote = zenquotes_data[0]['q']
  author = zenquotes_data[0]['a']

  # Use the GroupMe API to send the message
  requests.post(
      f"https://api.groupme.com/v3/bots/post",
      params={"access_token": ACCESS_TOKEN},
      json={
          "bot_id": bot_id,
          "text": f'"{quote}" - {author}',
      }
  )

# Schedule the send_message function to run every day at SEND_TIME
while True:
  # Get the current time
  current_time = datetime.datetime.now().strftime("%H:%M:%S")

  # If the current time is equal to the send time, run the send_message function
  if current_time == SEND_TIME:
    send_message()

  # Sleep for one minute before checking the time again
  time.sleep(43200)
  print(current_time)
