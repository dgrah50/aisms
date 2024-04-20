# SMS AI Chatbot

This project is an SMS AI Chatbot built using FastAPI, Twilio, and LangChain. It is designed to handle SMS interactions with users, providing functionalities like chat, account balance checking, resetting chat history, and fetching directions.

It's aimed at supporting dumbphones my providing basic needs over SMS. 

## Features

- **Chat**: Regular ChatGPT-style conversations over SMS.
- **Account Balance**: Check the user's account balance.
- **Reset Chat History**: Allows users to reset their conversation history.
- **Get Directions**: Users can request directions from one location to another.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8+
- pip and virtualenv
- Twilio Account and API credentials
- LangChain Account and API credentials

## Installation

Clone the repository:

```bash
git clone https://github.com/dgrah50/aisms
cd aisms
```


## Install dependencies Using poetry:

```bash
poetry install
```

## Environment Variables
Create a `.env` file in the root directory with the following variables:

```bash
OPENAI_API_KEY=your_openai_key
GMAPS_API_KEY=your_googlemaps_key
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
```

## Usage
To start the application, run:

```bash
poetry run start
```

This command starts the FastAPI server on `http://localhost:8000\` by default, and the server will reload automatically on code changes.

## API Routes

`POST /sms/`: Endpoint to receive SMS messages from Twilio and process based on the command or regular chat.
Security
Requests are authenticated using Twilio's request validation to ensure they are indeed coming from Twilio.

