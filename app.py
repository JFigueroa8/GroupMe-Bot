import requests
import random
import time
from datetime import date
from datetime import timedelta
from flask import Flask, request, jsonify
from config import access_token, bot_id, giphy_api_key, dad_api

app = Flask(__name__)

groupme_url = 'https://api.groupme.com/v3/bots/post'
giphy_url = f'http://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q='
zenquotes_url = 'https://zenquotes.io/api/random'
dad_jokes_url = 'https://icanhazdadjoke.com/slack'
chuck_norris_url = 'https://api.chucknorris.io/jokes/random'
nba_url = 'https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=basketball&league=nba'
nfl_url = 'https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl'


@app.route('/callback', methods=['POST', 'GET'])
def callback():
  data = request.get_json()
  text = data['text']
  name = data['name']
  sender_type = data['sender_type']

  headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
  }

  if sender_type != "user":
    return jsonify({'status': 'OK'}), 200

  if '$giphy' in text:
    text = text.replace('$giphy ', '').lower()
    giphy_data = requests.get(giphy_url + text).json()
    results_length = len(giphy_data['data'])
    random_index = random.randint(0, results_length - 1)
    gif = giphy_data['data'][random_index]['images']['original']['url']
    payload = {
      'bot_id': bot_id,
      'text': gif,
    }
    response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$quote' in text:
    zenquotes_data = requests.get(zenquotes_url).json()
    quote = zenquotes_data[0]['q']
    author = zenquotes_data[0]['a']
    payload = {
      'bot_id': bot_id,
      'text': f'"{quote}" - {author}',
    }
    response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$dad joke' in text:
    dad_jokes_data = requests.get(dad_jokes_url).json()
    fallback = dad_jokes_data['attachments'][0]['fallback']

    payload = {
      'bot_id': bot_id,
      'text': fallback,
    }
    response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$chuck' in text:
    chuck_norris_data = requests.get(chuck_norris_url).json()
    chuck_norris_joke = chuck_norris_data['value']

    payload = {
      'bot_id': bot_id,
      'text': chuck_norris_joke,
    }
    response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$nba yesterday' in text:
    today = date.today()
    yesterday = str(today - timedelta(days = 1))
    formatted_yesterday = '&dates=' + yesterday.replace('-', '')
    nba_data = requests.get(nba_url + formatted_yesterday).json()
    nba_games_list = []

    for event in nba_data['sports'][0]['leagues'][0]['events']:
      team1_name = event['competitors'][0]['displayName']
      team1_record = event['competitors'][0]['record']
      team1_score = event['competitors'][0]['score']
      team2_name = event['competitors'][1]['displayName']
      team2_record = event['competitors'][1]['record']
      team2_score = event['competitors'][1]['score']

      if int(team1_score) >= int(team2_score):
        nba_games_list.append(f'{team1_name} - {team1_score} - W\n({team1_record})\n{team2_name} - {team2_score} - L\n({team2_record})')
      else:
        nba_games_list.append(f'{team2_name} - {team2_score} - W\n({team2_record})\n{team1_name} - {team1_score} - L\n({team1_record})')
    
    for game in nba_games_list:
      payload = {
        'bot_id': bot_id,
        'text': game,
      }      
      response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$nba' in text:
    nba_data = requests.get(nba_url).json()
    nba_games_list = []

    for event in nba_data['sports'][0]['leagues'][0]['events']:
      team1_name = event['competitors'][0]['displayName']
      team1_record = event['competitors'][0]['record']
      team1_score = event['competitors'][0]['score']
      team2_name = event['competitors'][1]['displayName']
      team2_record = event['competitors'][1]['record']
      team2_score = event['competitors'][1]['score']

      if team1_score == '' and team2_score == '':
        nba_games_list.append(f'UPCOMING GAME\n{team1_name} - TBD\n({team1_record})\n{team2_name} - TBD\n({team2_record})')
      elif int(team1_score) >= int(team2_score):
        nba_games_list.append(f'{team1_name} - {team1_score} - W\n({team1_record})\n{team2_name} - {team2_score} - L\n({team2_record})')
      else:
        nba_games_list.append(f'{team2_name} - {team2_score} - W\n({team2_record})\n{team1_name} - {team1_score} - L\n({team1_record})')
    
    for game in nba_games_list:
      payload = {
        'bot_id': bot_id,
        'text': game,
      }      
      response = requests.post(groupme_url, json=payload, headers=headers)
  elif '$nfl' in text:
    nfl_data = requests.get(nfl_url).json()
    nfl_games_list = []

    for event in nfl_data['sports'][0]['leagues'][0]['events']:
      team1_name = event['competitors'][0]['displayName']
      team1_record = event['competitors'][0]['record']
      team1_score = event['competitors'][0]['score']
      team2_name = event['competitors'][1]['displayName']
      team2_record = event['competitors'][1]['record']
      team2_score = event['competitors'][1]['score']

      if team1_score == '' and team2_score == '':
        nfl_games_list.append(f'UPCOMING GAME\n{team1_name} - TBD\n({team1_record})\n{team2_name} - TBD\n({team2_record})')
      elif int(team1_score) >= int(team2_score):
        nfl_games_list.append(f'{team1_name} - {team1_score} - W\n({team1_record})\n{team2_name} - {team2_score} - L\n({team2_record})')
      else:
        nfl_games_list.append(f'{team2_name} - {team2_score} - W\n({team2_record})\n{team1_name} - {team1_score} - L\n({team1_record})')
    
    for game in nfl_games_list:
      payload = {
        'bot_id': bot_id,
        'text': game,
      }      
      response = requests.post(groupme_url, json=payload, headers=headers)
  else:
    return jsonify({'status': 'OK'}), 200

  return jsonify({'status': 'OK'}), 200

if __name__ == '__main__':
  app.debug = True
  app.run(port=3000)