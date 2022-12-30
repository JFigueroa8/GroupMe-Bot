import requests
from config import access_token, bot_id
from urls import groupme_url, chuck_norris_url

def chuck_joke():
  # Get the data from the Chuck Norris API
  chuck_norris_data = requests.get(chuck_norris_url).json()

  # Get the joke
  chuck_norris_joke = chuck_norris_data['value']

  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': chuck_norris_joke,
  }

  # Send the joke to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)