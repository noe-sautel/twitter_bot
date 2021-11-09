# tweepy-bots/bots/config.py
import tweepy
import logging
import os
import json

"""
Documentation links
https://docs.tweepy.org/en/latest/api.html
https://developer.twitter.com/en/portal/dashboard
"""
with open('credentials.json') as json_file:
    creds = json.load(json_file)

logger = logging.getLogger()

def create_api():
    consumer_key = creds["api_key"] # "CONSUMER_KEY"
    consumer_secret = creds["api_secret_key"] # "CONSUMER_SECRET"
    access_token = creds["acess_token"] # "ACCESS_TOKEN"
    access_token_secret = creds["acess_token_secret"] # "ACCESS_TOKEN_SECRET"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api