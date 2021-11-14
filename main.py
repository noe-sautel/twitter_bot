import tweepy
import logging
from config import create_api, textgears_api
import time
import datetime
from textgears import correct_text
import emoji

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        # print([tweet.text, tweet.user.name, tweet.id, tweet.in_reply_to_status_id])        
        if any(keyword in tweet.text for keyword in keywords):
            tweet_corrected = correct_text(tweet_text = tweet.text, user_tweet_name = tweet.user.name, api_key = textgears_api())
            api.update_status(status=tweet_corrected, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            logger.info(f"Answered to {tweet.user.name}")
            if not tweet.user.following :
                tweet.user.follow()
    return new_since_id

def main():
    api = create_api()
    since_id = 1448055110261673995 # 1
    while True:
        since_id = check_mentions(api, ["chocolat", "vert"], since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()