import tweepy
import logging
# import json
from os import environ

logger = logging.getLogger()

# with open('credentials.json') as json_file:
#     creds = json.load(json_file)

def create_api():
    consumer_key = environ.get('api_key') # creds["api_key"] # "CONSUMER_KEY"
    consumer_secret = environ.get('api_secret_key') # creds["api_secret_key"] # "CONSUMER_SECRET"
    access_token = environ.get('acess_token') # creds["acess_token"] # "ACCESS_TOKEN"
    access_token_secret = environ.get('acess_token_secret') # creds["acess_token_secret"] # "ACCESS_TOKEN_SECRET"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating Tweeter API", exc_info=True)
        raise e
    logger.info("Tweeter API created")
    return api

def textgears_api():
    try:
        logger.info("Textgears API created")
        return creds["textgears_api_key"]  # "TEXTGEARS_API"
    except Exception as e:
        logger.error("Error getting Textgears API", exc_info=True)
        raise e

def since_id_read():
    with open("since_id.text", "r") as fp:
        return int(fp.read())

def since_id_write(current_since_id):
    with open("since_id.text", "w") as fp:
        fp.write(str(current_since_id))