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

def grab_card_ids(character):
  card_ids = []
  card_ids.append(character)
   # Set the URL of the website
  url = f'https://marvelsnapzone.com/cards/{character}'

  # Send a request to the website and get the HTML code
  response = requests.get(url)
  html = response.text

  # Load the HTML code into a Beautiful Soup object
  soup = BeautifulSoup(html, 'html.parser')

  # Find all the div tags with the class "card-variants"
  div_tags = soup.find_all("div", {"class": "card-variants"})
  
  variant_card_links = []
  
  # Iterate over the div tags
  for div_tag in div_tags:
    # Find the h2 element within the div tag
    h2_element = div_tag.find("h2")
    # If the text of the h2 element is "Variants"
    if h2_element.text == "Variants":
      # Find all the a tags within the div tag
      a_tags = div_tag.find_all("a")
      # Extract the href attribute values from the a tags
      href_values = [a.get("href") for a in a_tags]
      # Add the href values to the list of variant card links
      variant_card_links.extend(href_values)

  for url in variant_card_links:
    
    # Extract the text from the sibling div tags then add it to the dictionary
    variant_id = url.split("/")
    variant_id = variant_id[-2]
    
    card_ids.append(variant_id)

  return card_ids

def grab_every_description(list_of_ids, character_name):
  character_description_list = []
  variant_image_urls_list = grab_image_urls(character_name)
  print('Length of variant_image_urls_list: ', len(variant_image_urls_list))
  print('Length of list_of_ids: ', len(list_of_ids))

  for count, id in enumerate(list_of_ids):
    # print(list_of_ids)
    character_description = {}
    if count == 0:
      # Make a request to the website and retrieve the HTML
      html = requests.get(f"https://marvelsnapzone.com/cards/{id}").text

      # Use Beautiful Soup to parse the HTML
      soup = BeautifulSoup(html, "html.parser")

      # Find all the a tags with the href attribute value that contains the character name
      a_tags = soup.find_all(href=re.compile(f"https://marvelsnapzone.com/cards/{id}"))
      
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
      character_description['card_id'] = id
      character_description['source'] = source_status_text
      character_description['image_url'] = a_tags[1]["data-cimg"]
      character_description_list.append(character_description)

    else:
      # Make a request to the website and retrieve the HTML
      html = requests.get(f"https://marvelsnapzone.com/variants/{id}").text

      # Use Beautiful Soup to parse the HTML
      soup = BeautifulSoup(html, "html.parser")

      # Find the div tag with the class "name" and the text "Status"
      div_tag_status = soup.find("div", text="Status")

      # Find the div tag with the class "name" and the text "Rarity"
      div_tag_rarity = soup.find("div", text="Rarity")

      # Find the sibling div tags
      status_sibling_div_tags = div_tag_status.find_next_siblings("div")

      # Get the text from the sibling div tag
      card_status_text = status_sibling_div_tags[0].text

      # Check if the div_tag_rarity is None, if it is then the card is an unreleased card and we'll assign it the card status text which should be "Unreleased"
      if div_tag_rarity == None:
        div_tag_rarity = card_status_text
        # print(id)
        character_description = {'card_id': id, 'status': card_status_text, 'rarity': div_tag_rarity, 'image_url': variant_image_urls_list[count-1]}
        character_description_list.append(character_description)
      else:
        # Find the sibling div tags and extract the text from the sibling div tags then add it to the dictionary
        rarity_sibling_div_tags = div_tag_rarity.find_next_siblings("div")
        card_rarity_text = rarity_sibling_div_tags[0].text
        character_description = {'card_id': id, 'status': card_status_text, 'rarity': card_rarity_text, 'image_url': variant_image_urls_list[count-1]}
        # Variant ID, Status, Rarity
        character_description_list.append(character_description)
  # print(character_description_list)
  return character_description_list

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

  for link in links:
    images = link.find_all('img', attrs={'data-src': True})

    for image in images:
      response = requests.get(image['data-src'])
      print(image)
      if response.status_code == 200:
        image_links.append(image['data-src'])
      else:
        print(f'Error for image {image} - {image["data-src"]}')
  
  return image_links

def grab_card_images(card_description_list):
  # Iterate over the list of card descriptions and grab the image URL
  for count, card in enumerate(card_description_list):
    # Send a GET request to the URL and save the response as a variable
    url = card['image_url']
    card_id = card['card_id']
    response = requests.get(url)
    
    # Open the response as an image using the Pillow library
    image = Image.open(BytesIO(response.content))
    # converting to jpg
    rgb_image = image.convert("RGB")
      
    # exporting the image
    rgb_image.save(f"images/{count}.jpg")



app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  sender_type = data['sender_type']

  # Remove all extra spaces
  def remove_all_extra_spaces(string):
      return " ".join(string.split())

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$snap' in text:
    text = text.replace('$snap ', '').lower()
    character_name = remove_all_extra_spaces(text)

    if ' ' in character_name:
      character_name = character_name.replace(' ', '-')

    card_ids = grab_card_ids(character_name)
    urls = grab_image_urls(character_name)

    # ******** WORKAROUND FOR HULK *******************
    if character_name == 'hulk':
      card_ids.pop()
      print(f'card_ids length - {len(card_ids)}')
      print(f'urls length - {len(urls)}')
    list_of_descriptions = grab_every_description(card_ids, character_name)
    grab_card_images(list_of_descriptions)

    image_url_list = []

    # directory for images
    directory = 'images'

    # iterate over files in that directory
    for filename in sorted(os.listdir(directory)):

      # get the size of the image in bytes
      image_size = os.stat('images/' + filename).st_size
      data = open('images/' + filename, 'rb').read()

      image_headers = {
        'Content-Type': 'image/jpeg',
        'Content-Length': str(image_size),
        'X-Access-Token': access_token
      }

      groupme_response = requests.post(url='https://image.groupme.com/pictures', data=data, headers=image_headers)
      image_url = groupme_response.json()['payload']['picture_url']
      image_url_list.append(image_url)
      
    for count, card in enumerate(list_of_descriptions):
      # print(card)
      card_status = card['status']
      card['groupme_image_url'] = image_url_list[count]
      card_groupme_url = card['groupme_image_url']
      card_id = card['card_id']

      if count == 0:
        if card['ability'] == None:
          card_ability = 'No card ability'
        else:
          card_ability = card['ability']

        card_source = card['source']
        card_name = card['name']

        main_card_headers = {
        'Content-Type': 'image/jpeg',
        'X-Access-Token': access_token,
        }

        main_card_payload = {
          'bot_id': bot_id,
          'text': filename,
          'text': f"Name: {card_name}\n\nAbility: {card_ability}\n\nStatus: {card_status}\n\nSource: {card_source}\nCard ID: {card_id}\n",
          'attachments': [
            {
            'type': 'image',
            'url': card_groupme_url,
            }
          ],
        }
        response = requests.post(groupme_url, json=main_card_payload, headers=main_card_headers)
      else:
        if card['rarity'] == None:
          card_rarity = card_status
        else:
          card_rarity = card['rarity']

        variant_card_headers = {
        'Content-Type': 'image/jpeg',
        'X-Access-Token': access_token,
        }

        variant_card_payload = {
          'bot_id': bot_id,
          'text': filename,
          'text': f"Status: {card_status}\n\nRarity: {card_rarity}\n\nCard ID: {card_id}\n",
          'attachments': [
            {
            'type': 'image',
            'url': card_groupme_url,
            }
          ],
        }
        response = requests.post(groupme_url, json=variant_card_payload, headers=variant_card_headers)
    
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