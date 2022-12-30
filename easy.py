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

  if '$easy' in text:
    headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
    }

    payload = {
      'bot_id': bot_id,
      'attachments': [
        {
          "type":"video",
          "preview_url":"https://v.groupme.com/88126238/2022-12-30T04:19:34Z/7d992d97.1080x1920r0.jpg",
          "url":"https://v.groupme.com/88126238/2022-12-30T04:19:34Z/7d992d97.1080x1920r0.mp4"
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