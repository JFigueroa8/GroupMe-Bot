import requests
import requests
import os
import random
import string
import re
from flask import Flask, request, jsonify
from config import access_token, bot_id
from urls import groupme_url, snap_search_url_2
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

def grab_image_urls(character):
  # Set the URL of the website
  url = f'https://marvelsnapzone.com/cards/{character}'

  # Send a request to the website and get the HTML code
  response = requests.get(url)
  html = response.text

  # Load the HTML code into a Beautiful Soup object
  soup = BeautifulSoup(html, 'html.parser')

  # Find all the <a> tags with the class "variant"
  links = soup.find_all('a', class_='variant')

  # Iterate over the links and find the images with the attribute "data-src"
  image_links = []
  default_image = f"https://marvelsnapzone.com/wp-content/themes/blocksy-child/assets/media/cards/{character}.webp?v=25"
  response = requests.get(default_image)
  if response.status_code == 200:
    image_links.append(default_image)

  for link in links:
    images = link.find_all('img', attrs={'data-src': True})
    for image in images:
      response = requests.get(image['data-src'])
      if response.status_code == 200:
        image_links.append(image['data-src'])
  return image_links

def grab_name_description(character_name):
  # Make a request to the website and retrieve the HTML
  html = requests.get(f"https://marvelsnapzone.com/cards/{character_name}").text
  caps_character_name = string.capwords(character_name)
  character_description = {}
  # Use Beautiful Soup to parse the HTML
  soup = BeautifulSoup(html, "html.parser")

  a_tags = soup.find_all(href=re.compile(f"https://marvelsnapzone.com/cards/{character_name}"))
  character_description['name'] = a_tags[1]["data-name"]
  character_description['ability'] = a_tags[1]["data-ability"]  

  return character_description

def grab_card_images(character_name, image_urls_list):
  # Iterate over the list of image URLs
  for count, url in enumerate(image_urls_list):
    # Send a GET request to the URL and save the response as a variable
    response = requests.get(url)
    
    # Open the response as an image using the Pillow library
    image = Image.open(BytesIO(response.content))
    # converting to jpg
    rgb_image = image.convert("RGB")
      
    # exporting the image
    rgb_image.save(f"images/{character_name}-{count}.jpg")

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

    if ' ' in character_name:
      character_name = character_name.replace(' ', '-')

    urls = grab_image_urls(character_name)
    description = grab_name_description(character_name)
    grab_card_images(character_name, urls)

    # directory for images
    directory = 'images'

    payload = {
        'bot_id': bot_id,
        'text': f"Name: {description['name']}\n\nAbility: {description['ability']}\n\n",
      }
    response = requests.post(groupme_url, json=payload, headers=headers)
 
    # iterate over files in that directory
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