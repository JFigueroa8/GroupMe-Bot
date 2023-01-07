from flask import Flask, request, jsonify
from commands.allen import allen_dance
from commands.jimmy import jimmy_images
from commands.giphy import grab_gif
from commands.quote import random_quote
from commands.dad_jokes import dad_joke
from commands.chuck_norris import chuck_joke
from commands.nba_yesterdays_scores import yesterdays_nba_scores
from commands.nba_scores import nba_scores
from commands.nfl_scores import nfl_scores
from commands.easy import its_easy_boys
from commands.saw_everything import saw_everything
from commands.tom_hanks import busy
from commands.defeated import defeated
from commands.snoop_who import snoop_who
from commands.tuga_laugh import tuga_laugh
from commands.clutch import clutch
from commands.steve_kick import kick
from commands.yeet import yeet
from commands.steve_splash import splash
from commands.commands_list import commands_list
from commands.shrimp import shrimp_images
from commands.madden import madden
from commands.spider_monkey import spider_monkey
from commands.mistakes import mistakes
from commands.footlong import footlong
from commands.middle_aged import middle_aged
from commands.comrade_dennis import comrade_dennis
from commands.fart import fart
from commands.king import king
from commands.gizmo import gizmo
from commands.latin_king import latin_king
from commands.snap import snap
from commands.suntanstupidman import suntanstupidman
from commands.confused import confused
from commands.cam import cam
from commands.grow_up import grow_up
from commands.dancing import dancing
from commands.disney_wait_times import disney_wait_times
from configuration.config import access_token, bot_id, giphy_api_key, group_id
from configuration.urls import groupme_url, giphy_url, zenquotes_url, dad_jokes_url, chuck_norris_url, nba_url, nfl_url

app = Flask(__name__)

@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  sender_type = data['sender_type']
  text = text.lower()

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$giphy' in text:
    grab_gif(text, access_token, bot_id, groupme_url, giphy_url, giphy_api_key)
  elif '$quote' in text:
    random_quote(access_token, bot_id, groupme_url, zenquotes_url)
  elif '$dad joke' in text:
    dad_joke(access_token, bot_id, groupme_url, dad_jokes_url)
  elif '$chuck' in text:
    chuck_joke(access_token, bot_id, groupme_url, chuck_norris_url)
  elif '$nba yesterday' in text:
    yesterdays_nba_scores(access_token, bot_id, groupme_url, nba_url)
  elif '$nba' in text:
    nba_scores(access_token, bot_id, groupme_url, nba_url)
  elif '$nfl' in text:
    nfl_scores(access_token, bot_id, groupme_url, nfl_url)
  elif '$best qb' in text or '$karma' in text:
    allen_dance(access_token, bot_id, groupme_url)
  elif '$jimmy' in text:
    jimmy_images(access_token, bot_id, groupme_url)
  elif '$easy' in text:
    its_easy_boys(access_token, bot_id, groupme_url)
  elif '$saw everything' in text:
    saw_everything(access_token, bot_id, groupme_url)
  elif '$busy' in text:
    busy(access_token, bot_id, groupme_url)
  elif '$defeated' in text:
    defeated(access_token, bot_id, groupme_url)
  elif '$who' in text:
    snoop_who(access_token, bot_id, groupme_url)
  elif '$laugh' in text:
    tuga_laugh(access_token, bot_id, groupme_url)
  elif '$clutch' in text:
    clutch(access_token, bot_id, groupme_url)
  elif '$kick' in text:
    kick(access_token, bot_id, groupme_url)
  elif '$yeet' in text:
    yeet(access_token, bot_id, groupme_url)
  elif '$splash' in text:
    splash(access_token, bot_id, groupme_url)
  elif '$commands' in text:
    commands_list(access_token, bot_id, groupme_url)
  elif '$shrimp' in text:
    shrimp_images(access_token, bot_id, groupme_url)
  elif '$madden' in text or '$champion' in text:
    madden(access_token, bot_id, groupme_url)
  elif '$spider monkey' in text or '$joe' in text or '$best promo' in text:
    spider_monkey(access_token, bot_id, groupme_url)
  elif '$mistakes' in text or '$blonde' in text:
    mistakes(access_token, bot_id, groupme_url)
  elif '$footlong' in text or '$meat to the face' in text:
    footlong(access_token, bot_id, groupme_url)
  elif '$middle aged' in text or '$ricky' in text:
    middle_aged(access_token, bot_id, groupme_url)
  elif '$comrade dennis' in text or '$dennis' in text:
    comrade_dennis(access_token, bot_id, groupme_url)
  elif '$fart' in text or '$rodney' in text or '$cory' in text:
    fart(access_token, bot_id, groupme_url)
  elif '$king' in text or '$wakanda' in text or '$black panther' in text:
    king(access_token, bot_id, groupme_url)
  elif '$gizmo' in text:
    gizmo(access_token, bot_id, groupme_url)
  elif '$super pause' in text:
    dancing(access_token, bot_id, groupme_url)
  elif 'pause' in text:
    grow_up(access_token, bot_id, groupme_url)
  elif '$confused' in text:
    confused(access_token, bot_id, groupme_url)
  elif '$cam' in text:
    cam(access_token, bot_id, groupme_url)
  elif '$suntanstupidman' in text:
    suntanstupidman(access_token, bot_id, groupme_url)
  elif '$latin king' in text or '$namor' in text:
    latin_king(access_token, bot_id, groupme_url)
  elif '$snap' in text:
    # Remove all extra spaces
    def remove_all_extra_spaces(string):
        return " ".join(string.split())

    text = text.replace('$snap ', '')
    character_name = remove_all_extra_spaces(text)

    if ' ' in character_name:
      character_name = character_name.replace(' ', '-')

    snap(character_name, access_token, bot_id, groupme_url)
  elif '$magic kingdom' in text:
    park_url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldMagicKingdom/waittime'

    # Remove all extra spaces
    def remove_all_extra_spaces(string):
        return " ".join(string.split())

    text = text.replace('$magic kingdom ', '')
    ride_name = remove_all_extra_spaces(text)

    disney_wait_times(access_token, bot_id, groupme_url, park_url, ride_name)
  elif '$epcot' in text:
    park_url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldEpcot/waittime'

    # Remove all extra spaces
    def remove_all_extra_spaces(string):
        return " ".join(string.split())

    text = text.replace('$epcot ', '')
    ride_name = remove_all_extra_spaces(text)

    disney_wait_times(access_token, bot_id, groupme_url, park_url, ride_name)
  elif '$hollywood studios' in text:
    park_url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldHollywoodStudios/waittime'

    # Remove all extra spaces
    def remove_all_extra_spaces(string):
        return " ".join(string.split())

    text = text.replace('$hollwood studios ', '')
    ride_name = remove_all_extra_spaces(text)

    disney_wait_times(access_token, bot_id, groupme_url, park_url, ride_name)
  elif '$animal kingdom' in text:
    park_url = 'https://api.themeparks.wiki/preview/parks/WaltDisneyWorldAnimalKingdom/waittime'

    # Remove all extra spaces
    def remove_all_extra_spaces(string):
        return " ".join(string.split())

    text = text.replace('$animal kingdom ', '')
    ride_name = remove_all_extra_spaces(text)

    disney_wait_times(access_token, bot_id, groupme_url, park_url, ride_name)
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)