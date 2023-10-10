import asyncio
import json
import logging
import os
from telegram import Bot

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get telegram bot token
TOKEN = os.environ['BOT_TOKEN']

async def send_telegram_message(chat_id, response):
    try:
        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        raise TelegramError(f"Error sending message: {str(e)}")

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))
        
        # Extract data from the event
        json_data = json.loads(event['body'])
        props = json_data.get('messageProps', {})
        
        if not props:
            raise ValueError("MessageProps not found in the event body")
        
        # Extract necessary properties
        chat_id = props.get('chatId')
        response = props.get('response')
        customer_name = props.get('customerName', '')
        
        if not chat_id or not response:
            raise ValueError("Chat ID or response not found in messageProps")
        
        
        # Respond to the message asynchronously
        asyncio.run(send_telegram_message(chat_id, response.format(customer_name= customer_name)))
        
        logging.info("Chatbot application running")
        
        # Return a successful response
        response = {
            'statusCode': 200,
            'body': json.dumps('Bot invoked to respond to the customer\'s message!')
        }
        return response
    
    except Exception as e:
        # Handle unexpected exceptions and raise a runtime error
        error_message = f"Unhandled error: {str(e)}"
        logger.error(error_message)
        raise RuntimeError(error_message)

class TelegramError(Exception):
    pass
