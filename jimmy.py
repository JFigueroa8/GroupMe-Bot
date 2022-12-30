import requests
import os
from config import access_token, bot_id
from urls import groupme_url

def jimmy_images():
  # Directory for images
  directory = 'jimmy_images'

  # Iterate over files in that directory
  for filename in os.listdir(directory):

    # Get the size of the image in bytes
    image_size = os.stat('jimmy_images/' + filename).st_size
    data = open('jimmy_images/' + filename, 'rb').read()

    # Set the headers for the first post request
    headers = {
      'Content-Type': 'image/jpeg',
      'Content-Length': str(image_size),
      'X-Access-Token': access_token}

    # Send the image to GroupMe image service
    groupme_response = requests.post(url='https://image.groupme.com/pictures', data=data, headers=headers)

    # Get the GroupMe image URL created by the GroupMe image service from the response
    image_url = groupme_response.json()['payload']['picture_url']

    # Set the headers for the second post request, which will send the image to GroupMe
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

    # Send the image to GroupMe
    response = requests.post(groupme_url, json=payload, headers=headers)