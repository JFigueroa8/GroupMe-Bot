import requests

def nfl_scores(access_token, bot_id, groupme_url, nfl_url):
  # Get the data from the ESPN API
  nfl_data = requests.get(nfl_url).json()

  nfl_games_list = []

  # Get the games, team names, scores, and records
  for event in nfl_data['sports'][0]['leagues'][0]['events']:
    team1_name = event['competitors'][0]['displayName']
    team1_record = event['competitors'][0]['record']
    team1_score = event['competitors'][0]['score']
    team2_name = event['competitors'][1]['displayName']
    team2_record = event['competitors'][1]['record']
    team2_score = event['competitors'][1]['score']

    # If the game has not started display TBD for the score
    # If team1 is leading in points during the game or after the game has finished, display team1 first, otherwise we'll display team2 first
    if team1_score == '' and team2_score == '':
      nfl_games_list.append(f'UPCOMING GAME\n{team1_name} - TBD\n({team1_record})\n{team2_name} - TBD\n({team2_record})')
    elif int(team1_score) >= int(team2_score):
      nfl_games_list.append(f'{team1_name} - {team1_score}\n({team1_record})\n{team2_name} - {team2_score}\n({team2_record})')
    else:
      nfl_games_list.append(f'{team2_name} - {team2_score}\n({team2_record})\n{team1_name} - {team1_score}\n({team1_record})')
  
  # Loop through the games
  for game in nfl_games_list:
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