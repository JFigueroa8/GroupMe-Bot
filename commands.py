import requests
from config import access_token, bot_id
from urls import groupme_url

def command_list():
  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': """$giphy <search term> - returns a random gif from Giphy using that search term

$quote - returns a random quote

$dad joke - returns a random dad joke for Cory, Steve and Jay

$chuck - returns a random Chuck Norris joke

$nba yesterday - returns yesterday's NBA scores

$nba - returns today's NBA scores

$nfl - returns NFL scores"""
  }

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)