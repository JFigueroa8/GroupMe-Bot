import requests
import os
import string
import re
import time
from flask import Flask, request, jsonify
from config import access_token, bot_id
from urls import groupme_url
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

def grab_main_card_description_status(character_name):
  # Make a request to the website and retrieve the HTML
  html = requests.get(f"https://marvelsnapzone.com/cards/{character_name}").text

  # Use Beautiful Soup to parse the HTML
  soup = BeautifulSoup(html, "html.parser")

  character_description = {}

  # Find all the a tags with the href attribute value that contains the character name
  a_tags = soup.find_all(href=re.compile(f"https://marvelsnapzone.com/cards/{character_name}"))
  print(a_tags[1])
  character_description['name'] = a_tags[1]["data-name"]
  if a_tags[1]["data-ability"] == "":
    character_description['ability'] = "No ability"
  else:
    character_description['ability'] = a_tags[1]["data-ability"]

  # Find the div tag with the text "Status"
  div_tag = soup.find("div", text="Status")

  # Find the sibling div tags
  status_sibling_div_tags = div_tag.find_next_siblings("div")

  # Find the div tag with the text "Source"
  div_tag = soup.find("div", text="Source")

  # Find the sibling div tags
  source_sibling_div_tags = div_tag.find_next_siblings("div")
  
  # Extract the text from the sibling div tags then add it to the dictionary
  card_status_text = status_sibling_div_tags[0].text
  character_description['status'] = card_status_text
  source_status_text = source_sibling_div_tags[0].text
  character_description['source'] = source_status_text

  return character_description

def grab_variant_status_rarity(variant_url_list):
  variant_status_rarity = []

  for url in variant_url_list:
    # Make a request to the website and retrieve the HTML
    html = requests.get(url).text
    
    # Use Beautiful Soup to parse the HTML
    soup = BeautifulSoup(html, "html.parser")  

    # Find the div tag with the class "name" and the text "Status"
    div_tag_status = soup.find("div", text="Status")

    # Find the div tag with the class "name" and the text "Rarity"
    div_tag_rarity = soup.find("div", text="Rarity")

    # Find the sibling div tags
    status_sibling_div_tags = div_tag_status.find_next_siblings("div")
    
    # Extract the text from the sibling div tags then add it to the dictionary
    variant_id = url.split("/")
    variant_id = variant_id[-2]

    # Get the text from the sibling div tag
    card_status_text = status_sibling_div_tags[0].text

    # Check if the div_tag_rarity is None, if it is then the card is an unreleased card and we'll assign it the card status text which should be "Unreleased"
    if div_tag_rarity == None:
      div_tag_rarity = card_status_text
      # variant_status_rarity[variant_id] = {'status': card_status_text, 'rarity': div_tag_rarity}
      variant_status_rarity.append([variant_id, card_status_text, div_tag_rarity])
    else:
      # Find the sibling div tags and extract the text from the sibling div tags then add it to the dictionary
      rarity_sibling_div_tags = div_tag_rarity.find_next_siblings("div")
      card_rarity_text = rarity_sibling_div_tags[0].text
      # variant_status_rarity[variant_id] = {'status': card_status_text, 'rarity': card_rarity_text}
      # Variant ID, Status, Rarity
      variant_status_rarity.append([variant_id, card_status_text, card_rarity_text])

  return variant_status_rarity

def grab_variant_page_links(character):
  # Set the URL of the website
  url = f'https://marvelsnapzone.com/cards/{character}'

  # Send a request to the website and get the HTML code
  response = requests.get(url)
  html = response.text

  # Load the HTML code into a Beautiful Soup object
  soup = BeautifulSoup(html, 'html.parser')

  # Find the div tag with the class "list-variants"
  div_tag = soup.find("div", {"class": "list-variants"})

  # Find all the a tags within the div tag
  a_tags = div_tag.find_all("a")

  # Extract the href attribute values from the a tags
  variant_card_links = [a.get("href") for a in a_tags]

  return variant_card_links

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

  # Remove all extra spaces
  def remove_all_extra_spaces(string):
      return " ".join(string.split())

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$snap' in text:
    text = text.replace('$snap ', '').lower()
    character_name = remove_all_extra_spaces(text)

    if ' ' in character_name:
      character_name = character_name.replace(' ', '-')

    urls = grab_image_urls(character_name)
    description = grab_main_card_description_status(character_name)
    grab_card_images(character_name, urls)
    variant_page_links = grab_variant_page_links(character_name)
    variant_status_rarity = grab_variant_status_rarity(variant_page_links)
    print(variant_status_rarity)
  
    image_url_list = []

    # directory for images
    directory = 'images'

    # iterate over files in that directory
    for filename in os.listdir(directory):

      # get the size of the image in bytes
      image_size = os.stat('images/' + filename).st_size
      data = open('images/' + filename, 'rb').read()

      headers_1 = {
        'Content-Type': 'image/jpeg',
        'Content-Length': str(image_size),
        'X-Access-Token': access_token
      }

      groupme_response = requests.post(url='https://image.groupme.com/pictures', data=data, headers=headers_1)
      image_url = groupme_response.json()['payload']['picture_url']
      image_url_list.append(image_url)

    headers_2 = {
    'Content-Type': 'image/jpeg',
    'X-Access-Token': access_token,
    }

    payload = {
      'bot_id': bot_id,
      'text': f"Name: {description['name']}\n\nAbility: {description['ability']}\n\nStatus: {description['status']}\n\nSource: {description['source']}",
      'attachments': [
        {
        'type': 'image',
        'url': image_url_list.pop(0),
        }
      ],
    }
    response = requests.post(groupme_url, json=payload, headers=headers_2)

    for count, url in enumerate(image_url_list):
      print(f'{count}-{url}')
      payload = {
        'bot_id': bot_id,
        'text': f"Status: {variant_status_rarity[count][1]}\n\nRarity: {variant_status_rarity[count][2]}\n",
        'attachments': [
          {
          'type': 'image',
          'url': url,
          }
        ],
      }
      response = requests.post(groupme_url, json=payload, headers=headers_2)

    # time.sleep(1)

    # payload2 = {
    #     'bot_id': bot_id,
    #     'text': f"Name: {description['name']}\n\nAbility: {description['ability']}\n\nStatus: {description['status']}\n",
    #   }
    # response = requests.post(groupme_url, json=payload2, headers=headers)
    
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