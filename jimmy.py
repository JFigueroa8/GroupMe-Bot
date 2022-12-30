import requests
import os
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

  if '$jimmy' in text:
    image_url_list = []

    # directory for images
    directory = 'jimmy_images'

    # iterate over files in that directory
    for filename in os.listdir(directory):

      # get the size of the image in bytes
      image_size = os.stat('jimmy_images/' + filename).st_size
      data = open('jimmy_images/' + filename, 'rb').read()
      headers={
        'Content-Type': 'image/jpeg',
        'Content-Length': str(image_size),
        'X-Access-Token': access_token}

      groupme_response = requests.post(url='https://image.groupme.com/pictures', data=data, headers=headers)
      image_url = groupme_response.json()['payload']['picture_url']
      image_url_list.append(image_url)

      headers = {
      'Content-Type': 'image/jpeg',
      'X-Access-Token': access_token,
      }

      payload = {
        'bot_id': bot_id,
        'attachments': [
          {
          'type': 'image',
          'url': image_url,
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