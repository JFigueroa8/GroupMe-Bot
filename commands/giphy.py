import requests
import random

def grab_gif(text, access_token, bot_id, groupme_url, giphy_url, giphy_api_key):
  # Set the entered text to lowercase and remove the command
  text = text.replace('$giphy ', '').lower()

  # Get the data from the Giphy API
  giphy_data = requests.get(f'{giphy_url}{giphy_api_key}&q={text}').json()

  # Get the length of the results and pick a random index
  results_length = len(giphy_data['data'])
  random_index = random.randint(0, results_length - 1)

  # Get the URL of the gif
  gif = giphy_data['data'][random_index]['images']['original']['url']

  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': gif,
  }

  # Send the gif to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)