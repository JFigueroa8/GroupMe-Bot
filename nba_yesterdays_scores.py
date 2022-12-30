import requests
from datetime import date, timedelta
from config import access_token, bot_id
from urls import groupme_url, nba_url

def yesterdays_nba_scores():
  # Get yesterday's date
  today = date.today()
  yesterday = str(today - timedelta(days = 1))

  # Format the date for the ESPN API
  formatted_yesterday = '&dates=' + yesterday.replace('-', '')

  # Get the data from the ESPN API
  nba_data = requests.get(nba_url + formatted_yesterday).json()
  
  nba_games_list = []

  # Get the games, team names, scores, and records
  for event in nba_data['sports'][0]['leagues'][0]['events']:
    team1_name = event['competitors'][0]['displayName']
    team1_record = event['competitors'][0]['record']
    team1_score = event['competitors'][0]['score']
    team2_name = event['competitors'][1]['displayName']
    team2_record = event['competitors'][1]['record']
    team2_score = event['competitors'][1]['score']

    # If team1's score is greater than team2's score, team1 won and we'll display team1 first, otherwise we'll display team2 first
    if int(team1_score) > int(team2_score):
      nba_games_list.append(f'{team1_name} - {team1_score} - W\n({team1_record})\n{team2_name} - {team2_score} - L\n({team2_record})')
    else:
      nba_games_list.append(f'{team2_name} - {team2_score} - W\n({team2_record})\n{team1_name} - {team1_score} - L\n({team1_record})')
  
  # Loop through the games
  for game in nba_games_list:
    # Set the headers and payload
    headers = {
    'Content-Type': 'application/json',
    'X-Access-Token': access_token,
    }

    payload = {
      'bot_id': bot_id,
      'text': game,
    }

    # Send the game to GroupMe
    response = requests.post(groupme_url, json=payload, headers=headers)