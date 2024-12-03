# Telegram Minion Bot

## Overview
This is a FastAPI-based Telegram bot application that supports multiple bot instances (main bot and minion bots) with webhook integration.

## Features
- Multiple Telegram bot support
- Webhook-based communication
- Dynamic bot token management
- SSL-secured NGINX configuration
- Docker containerization

## Project Structure
```
.
├── app/
│   ├── bot/
│   │   ├── handlers/
│   │   │   ├── __init__.py
│   │   │   ├── commands.py
│   │   │   ├── minions_commands.py
│   │   │   └── share_logic.py
│   │   ├── __init__.py
│   │   └── utils.py
│   ├── config.py
│   ├── constant.py
│   └── web/
│       ├── __init__.py
│       └── main.py
├── nginx/
│   ├── Dockerfile
│   ├── default.conf
│   └── ssl/
├── Dockerfile
├── docker-compose.yaml
└── requirements.txt
```

## Prerequisites
- Docker
- Docker Compose
- SSL Certificates (for HTTPS)

## Configuration
1. Create a `.env` file with the following variables:
   - `TOKEN`: Your Telegram bot token from [botfather](https://t.me/botfather)
   - `WEB_URL`: Your application's base URL (e.g. https://yourdomain.com)

## Installation
1. Clone the repository
2. Place SSL certificates in `nginx/ssl/`
    - `fullchain.pem` - SSL certificate
    - `privkey.pem` - SSL key
3. Run `docker-compose up --build`

## Endpoints
- `/webhook/telegram/main`: Main bot webhook
- `/webhook/telegram/{token}`: Minion bot webhooks

## Commands
- `/start`: Basic start command
- `/add_minion <TOKEN>`: Add a new minion bot

## Technologies
- FastAPI
- Aiogram
- NGINX
- Docker
- Docker Compose
- Python 3.9

## License
This project is licensed under the MIT License
