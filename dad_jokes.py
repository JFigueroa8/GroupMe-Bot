import requests
from config import access_token, bot_id
from urls import groupme_url, dad_jokes_url

def dad_joke():
  # Get the data from the Dad Jokes API
  dad_jokes_data = requests.get(dad_jokes_url).json()

  # Get the joke
  fallback = dad_jokes_data['attachments'][0]['fallback']

  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': fallback,
  }

  # Send the joke to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)