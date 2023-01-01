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
from tom_hanks import busy
from defeated import defeated
from snoop_who import snoop_who
from tuga_laugh import tuga_laugh
from clutch import clutch
from steve_kick import kick
from yeet import yeet
from steve_splash import splash
from commands import command_list

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
  elif '$busy' in text:
    busy()
  elif '$defeated' in text:
    defeated()
  elif '$who' in text:
    snoop_who()
  elif '$laugh' in text:
    tuga_laugh()
  elif '$clutch' in text:
    clutch()
  elif '$kick' in text:
    kick()
  elif '$yeet' in text:
    yeet()
  elif '$splash' in text:
    splash()
  elif '$command' in text:
    command_list()
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)