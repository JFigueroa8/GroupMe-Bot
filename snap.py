import requests
import os
import random
from flask import Flask, request, jsonify
from config import access_token, bot_id
from urls import groupme_url, snap_search_url, snap_image_url
from io import BytesIO
from PIL import Image

def grab_card_images(character, id_list):

  for id in id_list:
    # URL of the image you want to download
    image_url = f"https://images.marvelsnap.io/images/cards/{id}.webp"

    # Send a GET request to the URL and save the response as a variable
    response = requests.get(image_url)

    # Open the response as an image using the Pillow library
    image = Image.open(BytesIO(response.content))
    # converting to jpg
    rgb_image = image.convert("RGB")
      
    # exporting the image
    rgb_image.save(f"images/{character}-{id}.jpg")

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  sender_type = data['sender_type']

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$snap' in text:
    text = text.replace('$snap ', '').lower()
    character_name = text
    character_data = requests.get(f'{snap_search_url}{text}').json()
    default_card_id = []
    default_card_id.append(character_data['card'][0]['id'])

    if character_data['card'][0]['variants']:
      variants = character_data['card'][0]['variants'].split(',')
      card_ids = default_card_id + variants
    grab_card_images(character_name, card_ids)
    # print(card_ids)

    # directory for images
    directory = 'images'
 
    # iterate over files in that directory
    print(len(os.listdir(directory)))
    for filename in os.listdir(directory):

      # get the size of the image in bytes
      image_size = os.stat('images/' + filename).st_size
      data = open('images/' + filename, 'rb').read()
      headers={
        'Content-Type': 'image/jpeg',
        'Content-Length': str(image_size),
        'X-Access-Token': access_token}
      groupme_response = requests.post(url='https://image.groupme.com/pictures', data=data, headers=headers)
      image_url = groupme_response.json()['payload']['picture_url']

      headers = {
      'Content-Type': 'application/json',
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

  # Iterate over all the files in the directory
  for file in os.listdir(directory):
      # Construct the full file path
      file_path = os.path.join(directory, file)

      # Check if the file is a regular file (not a directory)
      if os.path.isfile(file_path):
          # Delete the file
          os.remove(file_path)

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)