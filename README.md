# GroupMe Bot

A feature-rich GroupMe bot built with Flask that responds to various commands with memes, jokes, sports scores, and entertainment content.

## Features

### 🎪 Entertainment & Memes
- **GIF Search**: Get GIFs from Giphy with custom search terms
- **Random Quotes**: Inspirational quotes to brighten your day
- **Dad Jokes**: Classic dad jokes for the group
- **Chuck Norris Facts**: Random Chuck Norris jokes
- **Meme Commands**: Various meme responses including Allen dance, Jimmy images, Shrimp images, and many more character-specific reactions

### 🏈 Sports
- **NBA Scores**: Get current NBA game scores
- **NBA Yesterday**: Yesterday's NBA game results
- **NFL Scores**: Current NFL game scores

### 🎢 Disney Park Wait Times
- **Magic Kingdom**: Check ride wait times at Magic Kingdom
- **EPCOT**: Check ride wait times at EPCOT
- **Hollywood Studios**: Check ride wait times at Hollywood Studios
- **Animal Kingdom**: Check ride wait times at Animal Kingdom

### 🎬 Marvel/Pop Culture
- **Snap Command**: Marvel character references
- **Various Character Commands**: Tom Hanks, Spider Monkey, Latin King, and many more

### 📅 Scheduled Features
- **Daily Quotes**: Automatic daily inspirational quotes at 8:00 AM EST

## Setup

### Prerequisites
- Python 3.7+
- GroupMe Developer Account
- Giphy API Account (optional, for GIF functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd GroupMe-Bot-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r configuration/requirements.txt
   ```

3. **Create configuration file**
   Create `configuration/config.py` with the following variables:
   ```python
   # GroupMe Configuration
   access_token = "YOUR_GROUPME_ACCESS_TOKEN"
   bot_id = "YOUR_BOT_ID"
   group_id = "YOUR_GROUP_ID"
   
   # Giphy Configuration (optional)
   giphy_api_key = "YOUR_GIPHY_API_KEY"
   ```

4. **Get your GroupMe credentials**
   - Visit [GroupMe Developers](https://dev.groupme.com/)
   - Create a new bot and note down your access token, bot ID, and group ID
   - (Optional) Get a Giphy API key from [Giphy Developers](https://developers.giphy.com/)

### Running the Bot

1. **Start the main application**
   ```bash
   python app.py
   ```
   The bot will run on `http://localhost:3000`

2. **Configure GroupMe webhook**
   - In your GroupMe bot settings, set the callback URL to your server's `/callback` endpoint
   - For local development, you may need to use ngrok or similar tunneling service

3. **Optional: Start the scheduler for daily quotes**
   ```bash
   python scheduler.py
   ```

## Usage

All bot commands start with `$` followed by the command name:

### Basic Commands
- `$commands` - Display list of available commands
- `$giphy <search term>` - Get a random GIF from Giphy
- `$quote` - Get a random inspirational quote
- `$dad joke` - Get a random dad joke
- `$chuck` - Get a random Chuck Norris joke

### Sports Commands
- `$nba` - Get today's NBA scores
- `$nba yesterday` - Get yesterday's NBA scores
- `$nfl` - Get NFL scores

### Disney Park Commands
- `$magic kingdom <ride name>` - Get wait time for a Magic Kingdom ride
- `$epcot <ride name>` - Get wait time for an EPCOT ride
- `$hollywood studios <ride name>` - Get wait time for a Hollywood Studios ride
- `$animal kingdom <ride name>` - Get wait time for an Animal Kingdom ride

### Meme & Character Commands
- `$best qb` or `$karma` - Allen dance
- `$jimmy` - Jimmy images
- `$easy` - "It's easy boys" response
- `$clutch` - Clutch response
- `$snap <character name>` - Marvel character snap reference
- And many more! (See the commands directory for full list)

## Project Structure

```
GroupMe-Bot-main/
├── app.py                  # Main Flask application
├── scheduler.py           # Daily quote scheduler
├── commands/             # Individual command modules
│   ├── giphy.py         # Giphy integration
│   ├── nba_scores.py    # NBA scores
│   ├── dad_jokes.py     # Dad jokes
│   └── ...              # Many more command modules
├── configuration/       # Configuration files
│   ├── requirements.txt # Python dependencies
│   ├── urls.py         # API URLs
│   └── config.py       # Bot credentials (create this)
└── README.md           # This file
```

## Dependencies
- **Flask**: Web framework for handling GroupMe webhooks
- **requests**: HTTP requests for API calls
- **beautifulsoup4**: HTML parsing for web scraping
- **Pillow**: Image processing capabilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new commands in the `commands/` directory
4. Update the command list in `commands/commands_list.py`
5. Add the command handler in `app.py`
6. Submit a pull request

## API Integrations

This bot integrates with several APIs:
- **GroupMe API**: Core messaging functionality
- **Giphy API**: GIF search and retrieval
- **ZenQuotes API**: Random inspirational quotes
- **Dad Jokes API**: Random dad jokes
- **Chuck Norris API**: Chuck Norris facts
- **ESPN API**: Sports scores (NBA/NFL)
- **ThemeParks Wiki API**: Disney park wait times

## License

This project is open source. Feel free to modify and distribute as needed.

## Support

If you encounter issues:
1. Check that all configuration variables are set correctly
2. Ensure your GroupMe webhook URL is properly configured
3. Verify that required APIs are accessible
4. Check the Flask application logs for error messages 