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
from test import hello
from shrimp import shrimp_images
from madden import madden
from spider_monkey import spider_monkey
from mistakes import mistakes
from footlong import footlong
from middle_aged import middle_aged
from comrade_dennis import comrade_dennis

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
  elif '$best qb' in text or '$karma' in text:
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
  elif '$commands' in text:
    command_list()
  elif '$hello' in text:
    hello()
  elif '$shrimp' in text:
    shrimp_images()
  elif '$madden' in text or '$champion' in text:
    madden()
  elif '$spider monkey' in text or '$joe' in text or '$best promo' in text:
    spider_monkey()
  elif '$mistakes' in text or '$blonde' in text:
    mistakes()
  elif '$footlong' in text or '$meat to the face' in text:
    footlong()
  elif '$middle_aged' in text or '$ricky' in text:
    middle_aged()
  elif '$comrade_dennis' in text or '$dennis' in text:
    comrade_dennis()
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)