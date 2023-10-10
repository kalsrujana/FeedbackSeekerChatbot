import json
import time
import logging
from textblob import TextBlob

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define chatbot templates
templates = {
    "hi_note" : "Hi {customer_name}, You have been a great customer. We would love to hear your feedback. Please reply with your review.",
    "ack" : "Great! Waiting for your precious feedback.",
    "thank_you_note" : "You're very welcome! It was our pleasure to hear from you. If you have more feedback to share, please don't hesitate to share with us. Have a great day!",
    "question" : "We lack the necessary information to provide a response to your inquiry at this time. Our support team will promptly reach out to you for further assistance.",
    "strong_positive" : "Thank you so much for your positive feedback! We're thrilled to hear that you had a great experience with our product/service. Your satisfaction is our top priority, and we look forward to serving you again in the future. If you have any more feedback or suggestions, please feel free to share them with us.",
    "above_neutral" : "Sure! We respect your feedback.",
    "below_neutral" : "Your feedback is valuable, and we're committed to improving. We'd like to learn more about your concerns and work towards a solution. Please reach out to our support team so that we can assist you further.",
    "strong_negative" : "We're sorry to hear that you had a less than satisfactory experience with our product/service. Your feedback is valuable to us, and we're committed to improving. We'd like to learn more about your concerns and work towards a solution. Please reach out to our support team so that we can assist you further.",
    "neutral" : "Thank you for your feedback. We appreciate your input, and it helps us understand your experience better. If you have any specific suggestions or concerns you'd like to share, please don't hesitate to let us know. We're here to assist you and continuously enhance our offerings."
}

# Define trigger keywords
trigger_keywords = {
    # "transaction_completed": ["completed transaction", "purchase", "order"],
    "thank_you_note": ["thank you", "thanks"],
    "hi_note" : ["hi", "/start"],
    "ack" :  ["ok", "okay", "got it", "gotcha", "sure", "alright", "fine", "yes", "yep", "you too"],
    "question" : ["what", "why", "when", "?", "how"]
}

class MessageProcessor:
    def __init__(self, templates, trigger_keywords, logger):
        self.templates = templates
        self.trigger_keywords = trigger_keywords
        self.logger = logger

    def analyze_sentiment(self, message):
        try:
            # Create a TextBlob object and correct spelling
            blob = TextBlob(message)
            message = blob.correct()

            # Analyze sentiment (polarity) and subjectivity of the message
            sentiment_score = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity
            self.logger.debug(f"sentiment_polarity and sentiment.subjectivity of {message} is {sentiment_score} and {sentiment_subjectivity}")

            # Define thresholds for sentiment categories
            strong_positive_threshold = 0.2
            above_neutral_threshold = 0.1
            below_neutral_threshold = -0.1
            strong_negative_threshold = -0.2
            sub_threshold = 0.7

            # Determine the sentiment label based on polarity and subjectivity
            if sentiment_score > strong_positive_threshold and sentiment_subjectivity > sub_threshold:
                return "strong_positive"
            elif sentiment_score > above_neutral_threshold:
                return "above_neutral"
            elif sentiment_score < strong_negative_threshold and sentiment_subjectivity > sub_threshold:
                return "strong_negative"
            elif sentiment_score < below_neutral_threshold:
                return "below_neutral"
            else:
                return "neutral"
        except Exception as e:
            # Handle any exceptions that may occur during sentiment analysis
            self.logger.error(f"Error analyzing sentiment: {str(e)}")
            return "unknown_sentiment"

    def generate_response(self, message, feedback_range, chat_id, customer_name):
        is_feedback = True
        response = None
        if feedback_range == 'neutral':
            for keyword, keywords_list in self.trigger_keywords.items():
                for keyword, keywords_list in self.trigger_keywords.items():
                    if any(kw in message for kw in keywords_list):
                        is_feedback = False
                        response = self.templates[keyword]
                        break
            if not response:
                response = self.templates[feedback_range]
        else:
            response = self.templates[feedback_range]
        if not response:
            is_feedback = False
            response = "I'm sorry, I didn't understand your message."
        return {
            'feedbackMessage': message,
            'response': response,
            'feedbackRange': feedback_range,
            'isFeedback': is_feedback,
            'chatId' : chat_id,
            'customerName' : customer_name
        }

class S3ObjectBuilder:
    def __init__(self):
        self.S3_BUCKET_NAME = "chatbot-customer-feedback"

    def build_props_for_s3(self, message, chat_id, feedback_range):
        timestamp = time.time()
        feedback = {
            'customerId': chat_id,
            'feedbackMessage': message,
            'feedbackType': feedback_range,
            'timestamp': timestamp
        }
        # Generate a unique object key (e.g., using customer ID and timestamp)
        object_key = f'{feedback["customerId"]}/{feedback["customerId"]}_{feedback["feedbackType"]}_{feedback["timestamp"]}.json'
        # Convert feedback data to JSON format
        feedback_json = json.dumps(feedback)

        return {
            'Bucket': self.S3_BUCKET_NAME,
            'Key': object_key,
            'Body': feedback_json,
            'ContentType': 'application/json'
        }

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        # Retrieve data
        message = event['message']['text'].lower()
        chat_id = event['message']['chat']['id']
        customer_name = event['message']['chat']['first_name'] + " " + event['message']['chat']['last_name']

        message_processor = MessageProcessor(templates, trigger_keywords, logger)
        feedback_range = message_processor.analyze_sentiment(message)
        messageProps = message_processor.generate_response(message, feedback_range, chat_id, customer_name)

        s3_object_builder = S3ObjectBuilder()
        s3_props = {}
        if messageProps['isFeedback']:
            s3_props = s3_object_builder.build_props_for_s3(message, chat_id, feedback_range)

        logger.debug(messageProps)
        logger.debug(s3_props)
        return {
            'statusCode': 200,
            'isFeedback': messageProps['isFeedback'],
            'body': json.dumps({
                'messageProps': messageProps,
                's3Props': s3_props
            })
        }
    except Exception as e:
        # Handle unexpected exceptions and raise a runtime error
        error_message = f"Unhandled error: {str(e)}"
        logger.error(error_message)
        raise RuntimeError(error_message)
