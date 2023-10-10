from telegram import Bot
from telegram.error import TelegramError
import asyncio
import json
import os
import logging

# Get telegram bot token from environment variable
TOKEN = os.environ['BOT_TOKEN']

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class EventProcessor:
    def __init__(self, bot):
        self.bot = bot
    
    def get(self, event_type, event):
        if event_type == 'MODIFY':
            user_id = event['Records'][0]['dynamodb']['OldImage']['user_id']['N']
            old_status = event['Records'][0]['dynamodb']['OldImage']['transaction_status']['S']
            new_status = event['Records'][0]['dynamodb']['NewImage']['transaction_status']['S']
            if old_status != new_status and new_status.lower() == "completed":
                return TransactionCompleteEventProcessor(self.bot, user_id, old_status, new_status)
        # More event processors for different event types can be added here
        logger.info("Processor not implemented for the event type")
        return None

class TransactionCompleteEventProcessor:
    def __init__(self, bot, user_id, old_status, new_status):
        self.bot = bot
        self.user_id = user_id
        self.old_status = old_status
        self.new_status = new_status
    
    async def send_message(self, message_text):
        try:
            user = await self.bot.get_chat(self.user_id)
            first_name = user.first_name
            last_name = user.last_name
            formatted_message = message_text.format(first_name=first_name, last_name=last_name)
            await self.bot.send_message(chat_id=self.user_id, text=formatted_message)
            logger.debug('Message sent successfully!')
        except TelegramError as e:
            logger.error(f'Message sending failed: {e}')
    
    def process(self, event):
        logger.info(f"There is a change in transaction_status of user id: {self.user_id} from {self.old_status} to {self.new_status}")
        logger.debug("Triggering the chatbot")
        
        message_text = "Hi, {first_name} {last_name}, Thank you for your recent purchase! We would love to hear your feedback. Please reply with your review."
        
        # Run the asynchronous function to send the message
        asyncio.run(self.send_message(message_text))

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))
        event_type = event['Records'][0]['eventName']
        bot = Bot(token=TOKEN)
        event_processor = EventProcessor(bot).get(event_type, event)
        if event_processor:
            event_processor.process(event)
        return {
            'statusCode': 200,
            'body': json.dumps('Trigger sent to telegram user!')
        }
    except Exception as e:
        # Handle unexpected exceptions and raise a runtime error
        error_message = f"Unhandled error: {str(e)}"
        logger.error(error_message)
        raise RuntimeError(error_message)
