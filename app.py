import requests
import random
import time
from flask import Flask, request, jsonify
from config import access_token, bot_id, giphy_api_key, dad_api

app = Flask(__name__)

groupme_url = 'https://api.groupme.com/v3/bots/post'
giphy_url = f'http://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q='
zenquotes_url = 'https://zenquotes.io/api/random'
dad_jokes_url = 'https://icanhazdadjoke.com/slack'


@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  name = data['name']
  sender_type = data['sender_type']

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$giphy' in text:
    text = text.replace('$giphy ', '').lower()
    giphy_data = requests.get(giphy_url + text).json()
    results_length = len(giphy_data['data'])
    random_index = random.randint(0, results_length - 1)
    gif = giphy_data['data'][random_index]['images']['original']['url']
    payload = {
      'bot_id': bot_id,
      'text': gif,
    }
  elif '$quote' in text:
    zenquotes_data = requests.get(zenquotes_url).json()
    quote = zenquotes_data[0]['q']
    author = zenquotes_data[0]['a']
    payload = {
      'bot_id': bot_id,
      'text': f'"{quote}" - {author}',
    }
  elif '$dad joke' in text:
    dad_jokes_data = requests.get(dad_jokes_url).json()
    fallback = dad_jokes_data['attachments'][0]['fallback']

    payload = {
      'bot_id': bot_id,
      'text': fallback,
    }
  else:
    return jsonify({'status': 'OK'}), 200

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  response = requests.post(groupme_url, json=payload, headers=headers)
  
  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)