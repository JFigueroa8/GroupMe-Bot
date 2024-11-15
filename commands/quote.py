import requests

def random_quote(access_token, bot_id, groupme_url, zenquotes_url):
  # Get the data from the ZenQuotes API
  zenquotes_data = requests.get(zenquotes_url).json()

  # Get the quote and author
  quote = zenquotes_data[0]['q']
  author = zenquotes_data[0]['a']

  # Set the headers and payload
  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  payload = {
    'bot_id': bot_id,
    'text': f'"{quote}" - {author}',
  }

  # Send the quote to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)