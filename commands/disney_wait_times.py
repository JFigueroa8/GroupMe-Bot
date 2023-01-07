import requests
import string

def disney_wait_times(access_token, bot_id, groupme_url, park_url, ride_name):
  wait_times = []

  response = requests.get(park_url)
  park_data = response.json()

  for attraction in park_data:
    if attraction['meta']['type'] == 'ATTRACTION' and attraction['waitTime'] != None:
      attraction['name'] = attraction['name'].lower()
      
      if ride_name in attraction['name']:
        text = f"Name: {string.capwords(attraction['name'])}\nWait Time: {attraction['waitTime']}"
  if len(wait_times) == 0:
    text = 'No wait times available'
  
  # Set the headers and payload
  headers = {
      'Content-Type': 'application/json',
      'X-Access-Token': access_token,
  }

  payload = {
      'bot_id': bot_id,
      'text': text,
  }

  # Send the game to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)