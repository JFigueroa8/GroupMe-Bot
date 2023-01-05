import requests
import os
import re
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

def grab_card_ids(character, response):
  card_ids = []
  card_ids.append(character)
  
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

def grab_every_description(card_ids, main_card_url, main_card_response):
  character_description_list = []
  variant_image_urls_list = grab_image_urls(main_card_response)

  for count, id in enumerate(card_ids):
    character_description = {}
    if count == 0:
      html = main_card_response.text
      
      # Use Beautiful Soup to parse the HTML
      soup = BeautifulSoup(html, "html.parser")

      # Find all the a tags with the href attribute value that contains the character name
      a_tags = soup.find_all(href=re.compile(main_card_url))
      
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
      variant_url = f"https://marvelsnapzone.com/variants/{id}"
      
      # Make a request to the website and retrieve the HTML
      html = requests.get(variant_url).text
      
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

      if variant_image_urls_list[count-1] == 'error':
        continue
      else:
        # Check if the div_tag_rarity is None, if it is then the card is an unreleased card and we'll assign it the card status text which should be "Unreleased"
        if div_tag_rarity == None:
          div_tag_rarity = card_status_text
          character_description = {'card_id': id, 'status': card_status_text, 'rarity': div_tag_rarity, 'image_url': variant_image_urls_list[count-1]}
          character_description_list.append(character_description)

        else:
          # Find the sibling div tags and extract the text from the sibling div tags then add it to the dictionary
          rarity_sibling_div_tags = div_tag_rarity.find_next_siblings("div")
          card_rarity_text = rarity_sibling_div_tags[0].text
          character_description = {'card_id': id, 'status': card_status_text, 'rarity': card_rarity_text, 'image_url': variant_image_urls_list[count-1]}
          character_description_list.append(character_description)
  
  return character_description_list

def grab_image_urls(response):
  # Extract the HTML code from the response 
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
      
      if response.status_code == 200:
        image_links.append(image['data-src'])
      else:
        image_links.append('error')
  
  return image_links

def grab_card_images(card_description_list):
  # Iterate over the list of card descriptions and grab the image URL
  for count, card in enumerate(card_description_list):
    # Send a GET request to the URL and save the response as a variable
    url = card['image_url']
    
    response = requests.get(url)
    
    # Open the response as an image using the Pillow library
    image = Image.open(BytesIO(response.content))

    # converting to jpg
    rgb_image = image.convert("RGB")
      
    # exporting the image
    rgb_image.save(f"images/{count}.jpg")

def snap(character_name, access_token, bot_id, groupme_url):
    main_card_url = f'https://marvelsnapzone.com/cards/{character_name}'
    main_card_response = requests.get(main_card_url)

    card_ids = grab_card_ids(character_name, main_card_response)
    list_of_descriptions = grab_every_description(card_ids, main_card_url, main_card_response)
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

    # Iterate over all the files in the directory
    for file in os.listdir(directory):
        # Construct the full file path
        file_path = os.path.join(directory, file)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            # Delete the file
            os.remove(file_path)