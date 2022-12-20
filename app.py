import requests
from flask import Flask, request, jsonify
from config import access_token, bot_id

app = Flask(__name__)

url = 'https://api.groupme.com/v3/bots/post'

@app.route('/')

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  name = data['name']
  sender_type = data['sender_type']

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if 'giphy' in text:
    text = text.replace('giphy ', '').capitalize()
    payload = {
      'bot_id': bot_id,
      'text': f'You said: {text}',
    }
  else:
    return jsonify({'status': 'OK'}), 200

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token
  }

  response = requests.post(url, json=payload, headers=headers)
  

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)
