import requests

def groupme_2022_recap(access_token, bot_id, groupme_url):
  # Set the headers and payload
  headers = {
      'Content-Type': 'application/json',
      'X-Access-Token': access_token,
  }

  payload = {
      'bot_id': bot_id,
      'text': """2022 GroupMe Recap

You guys were a very talkative group last year. The total number of messages sent in 2022 was 41,273. That's a lot of messages. Here is a list with everyone's message count for last year:

Ricky: 9318,
Steven: 7116,
Shyste: 3934 (most of these were text messages, bless his heart),
Cory: 3810,
Jay: 3409,
Joe: 2873, 
Derek: 2627,
Rodney: 2339, 
Dennis: 2575,
Julmar: 2130,
Fabs: 1142"""
}

  # Send the image to GroupMe
  response = requests.post(groupme_url, json=payload, headers=headers)
