import tweepy
import logging
import config
import time
import textgears
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

auth_user_list = ['ohmyxan', 'noesautel']
# def check_mentions_keywords(api, keywords, since_id):
#     logger.info("Retrieving mentions")
#     new_since_id = since_id
#     for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
#         new_since_id = max(tweet.id, new_since_id)
#         # print([tweet.text, tweet.user.name, tweet.id, tweet.in_reply_to_status_id])        
#         if any(keyword in tweet.text for keyword in keywords):
#             tweet_corrected = textgears.correct_text(tweet_text = tweet.text, user_tweet_name = tweet.user.name, api_key = textgears_api())
#             api.update_status(status=tweet_corrected, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
#             logger.info(f"Answered to {tweet.user.name}")
#             if not tweet.user.following :
#                 tweet.user.follow()
#     return new_since_id

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = config.since_id_read()

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        print([tweet.text, tweet.user.name, tweet.id, tweet.in_reply_to_status_id])
        if not tweet.in_reply_to_status_id:
            continue
        elif api.get_status(tweet.in_reply_to_status_id).user.screen_name in auth_user_list :
            tweet_typo_prepared = api.get_status(tweet.in_reply_to_status_id).text
            tweet_typo = ' '.join(re.sub("(@[A-Za-z0-9_À-ÿ]+)|([^0-9A-Za-z_À-ÿ \t])|(\w+:\/\/\S+)"," ", tweet_typo_prepared).split())
            # # if any(keyword in tweet.text for keyword in keywords):
            tweet_corrected = textgears.correct_text(tweet_text = tweet_typo, user_tweet_name = tweet.user.name, api_key = config.textgears_api())
            try :
                api.update_status(status=tweet_corrected, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
            except tweepy.errors.HTTPException as error:
                if error.api_codes == [187]: # tweepy.errors.Forbidden: 403 Forbidden 187 - Status is a duplicate
                    logger.info("Duplicate tweet")
                    continue
                else:
                    raise error
            logger.info(f"Answered to {tweet.user.name}")
            if not tweet.user.following and tweet.user.name != 'Noé' :
                tweet.user.follow()
                logger.info(f"user @{tweet.user.name} has just been followed" )

        config.since_id_write(current_since_id=new_since_id)
        return new_since_id

def main():
    api = config.create_api()
    since_id = config.since_id_read()
    while True:
        # since_id = check_mentions_keywords(api, ["chocolat", "vert"], since_id)
        check_mentions(api=api, since_id=since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()