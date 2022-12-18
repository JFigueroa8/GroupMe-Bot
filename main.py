from flask import Flask, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROUP_NAME = os.getenv("GROUP_NAME")
BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")


# url = f"https://api.groupme.com/v3/bots/post?bot_id={BOT_ID}"

app = Flask(__name__)

GIPHY_API_KEY = os.getenv("GIPHY_KEY")
GROUPME_API_TOKEN = os.getenv("GROUPME_API_TOKEN")

def search_gif(query):
    response = requests.get(f'http://api.giphy.com/v1/gifs/search?q={query}&api_key={GIPHY_API_KEY}')
    if response.status_code == 200:
        gif_data = response.json()
        gif_url = gif_data['data'][0]['url']
        return gif_url

def send_message(sender_id, message_text):
    payload = {
        'bot_id': BOT_ID,
        'text': message_text
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=payload)

def send_gif(sender_id, gif_url):
    payload = {
        'bot_id': BOT_ID,
        'attachments': [{
            'type': 'image',
            'url': gif_url
        }]
    }
    requests.post('https://api.groupme.com/v3/bots/post', json=payload)

@app.route('/callback', methods=['POST'])
def receive_message():
    request_data = request.get_json()
    message_text = request_data['text']
    sender_id = request_data['sender_id']
    
    gif_url = search_gif(message_text)
    if gif_url:
        send_gif(sender_id, gif_url)
    else:
        send_message(sender_id, "Sorry, I couldn't find a GIF for that message.")

if __name__ == '__main__':
    app.run()