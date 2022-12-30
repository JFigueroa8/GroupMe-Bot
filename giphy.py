import requests
import random
from config import access_token, bot_id, giphy_api_key
from urls import groupme_url, giphy_url

def grab_gif(text):
  #Set the entered text to lowercase and remove the command
  text = text.replace('$giphy ', '').lower()

  #Get the data from the Giphy API
  giphy_data = requests.get(f'{giphy_url}{giphy_api_key}&q={text}').json()

  #Get the length of the results and pick a random index
  results_length = len(giphy_data['data'])
  random_index = random.randint(0, results_length - 1)

  #Get the URL of the gif
  gif = giphy_data['data'][random_index]['images']['original']['url']

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': gif,
  }
  response = requests.post(groupme_url, json=payload, headers=headers)