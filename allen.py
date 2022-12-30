import requests
from flask import Flask, request, jsonify
from config import access_token, bot_id
from urls import groupme_url

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  sender_type = data['sender_type']

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$allen' in text:
    headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
    }

    payload = {
      'bot_id': bot_id,
      'attachments': [
        {
          "type":"image",
          "url":"https://i.groupme.com/330x200.gif.9de6ba82c66a4a7c86b4f6be307b731e"
        }
      ],
    }
    response = requests.post(groupme_url, json=payload, headers=headers)
    
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)