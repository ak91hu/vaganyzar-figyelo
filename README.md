# MÁV Track Closure Discord Bot

A Python-based bot that monitors the MÁV track closure page and sends new track closure notifications to a Discord channel using a webhook.

## Features

* Periodically fetches the MÁV track closure page.
* Detects new PDF announcements about track closures.
* Sends Discord notifications with start and end dates, and a link to the PDF.
* Keeps track of already sent notifications to avoid duplicates.

## Requirements

* Python 3.12+
* Requests
* BeautifulSoup4
* Discord Webhook URL

## Setup

1. Clone the repository.
2. Set up environment variables:

```bash
export DISCORD_WEBHOOK=<your_discord_webhook_url>
export CHECK_INTERVAL=3600  # optional, default is 3600 seconds (1 hour)
export DATA_PATH=/data
```

3. Install dependencies:

```bash
pip install requests beautifulsoup4
```

## Running the Bot

To start the bot:

```bash
python3 mav_vaganyzar_discord.py
```

The bot will perform an initial check immediately and then continue checking the page periodically based on `CHECK_INTERVAL`.

## Docker Usage

1. Build the Docker image:

```bash
docker build -t mav-vaganyzar-bot .
```

2. Run the Docker container:

```bash
docker run -d --name mav-vaganyzar-bot -e DISCORD_WEBHOOK=<your_webhook_url> mav-vaganyzar-bot
```

3. To stop the container:

```bash
docker stop mav-vaganyzar-bot
```

4. To remove the container:

```bash
docker rm mav-vaganyzar-bot
```

## Notes

* Make sure the Discord webhook is correctly configured.
* The bot maintains a JSON file to store already sent PDF links to avoid duplicate notifications.
* Logs are printed to the console.

## Credits

* Vibe coding session inspired this bot.
* Developed with help from ChatGPT
