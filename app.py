from flask import Flask, request, jsonify
from allen import allen_dance
from jimmy import jimmy_images
from giphy import grab_gif
from quote import random_quote
from dad_jokes import dad_joke
from chuck_norris import chuck_joke
from nba_yesterdays_scores import yesterdays_nba_scores
from nba_scores import nba_scores
from nfl_scores import nfl_scores
from easy import its_easy_boys
from saw_everything import saw_everything

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  sender_type = data['sender_type']

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$giphy' in text:
    grab_gif(text)
  elif '$quote' in text:
    random_quote()
  elif '$dad joke' in text:
    dad_joke()
  elif '$chuck' in text:
    chuck_joke()
  elif '$nba yesterday' in text:
    yesterdays_nba_scores()
  elif '$nba' in text:
    nba_scores()
  elif '$nfl' in text:
    nfl_scores()
  elif '$best qb' in text:
    allen_dance()
  elif '$jimmy' in text:
    jimmy_images()
  elif '$easy' in text:
    its_easy_boys()
  elif '$saw everything' in text:
    saw_everything()
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)