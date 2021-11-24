import tweepy
import logging
import emoji
import config
import time
import textgears
import re
from PIL import Image, ImageChops
import requests
from io import BytesIO


logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(message)s", 
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

auth_user_list = ['ohmyxan']
not_follow_self = ['narcoticsqueed', 'noesautel', 'ohmyxan_nemesis']

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = config.since_id_read()

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id = since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        logging.info(f"CURSOR : text:{tweet.text}, user.name:{tweet.user.name}, id:{tweet.id}, in_reply_to_status_id:{tweet.in_reply_to_status_id}")
        if not tweet.in_reply_to_status_id:
            continue
        elif api.get_status(tweet.in_reply_to_status_id).user.screen_name not in auth_user_list and any(keyword in tweet.text for keyword in keywords):
            try :
                api.update_status(status=f"Désolé, mais je ne corrige que les tweets de @ohmyxan {emoji.emojize(':blue_heart:')}", in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                logger.info(f"Answered to {tweet.user.name} on {tweet.id} with @ohmyxan filter")       
            except tweepy.errors.HTTPException as error:
                if error.api_codes == [187]: # tweepy.errors.Forbidden: 403 Forbidden 187 - Status is a duplicate
                    logger.warning(f"Duplicate tweet {tweet.id}.")
                    continue
                else:
                    raise error
        elif api.get_status(tweet.in_reply_to_status_id).user.screen_name in auth_user_list and any(keyword in tweet.text for keyword in keywords):
            tweet_typo_prepared = api.get_status(tweet.in_reply_to_status_id).text
            tweet_typo = ' '.join(re.sub("(@[A-Za-z0-9_À-ÿ]+)|([^0-9A-Za-z_À-ÿ \t])|(\w+:\/\/\S+)"," ", tweet_typo_prepared).split())
            tweet_corrected = textgears.correct_text(tweet_text = tweet_typo, api_key = config.textgears_api())
            try :
                api.update_status(status=tweet_corrected, in_reply_to_status_id=tweet.id, auto_populate_reply_metadata=True)
                logger.info(f"Answered to {tweet.user.name} on {tweet.id}: {tweet_corrected}.")                
            except tweepy.errors.HTTPException as error:
                if error.api_codes == [187]: # tweepy.errors.Forbidden: 403 Forbidden 187 - Status is a duplicate
                    logger.warning(f"Duplicate tweet {tweet.id}")
                    continue
                else:
                    raise error
        if not tweet.user.following and tweet.user.screen_name not in not_follow_self:
            tweet.user.follow()
            logger.info(f"User @{tweet.user.name} has just been followed" )

        config.since_id_write(current_since_id=new_since_id)
        return new_since_id

def invert_image(api, user):
    try:
        lookup_user = api.lookup_users(screen_name=[user])[0]
        img_raw = ''.join(re.sub("_normal"," ", lookup_user.profile_image_url_https).split()) # le retrait de _normal permet de passer en 400*400px au lieu d'une miniature
        response = requests.get(img_raw)
        img = Image.open(BytesIO(response.content))
        inv_img = ImageChops.invert(img)
        im1 = Image.open('profile_picture.jpg')
        inv_img.save('profile_picture.jpg')
        im2 = Image.open('profile_picture.jpg')
        if list(im1.getdata()) == list(im2.getdata()):
            logger.warning("Profile picture identical ; no update.")
        else:
            api.update_profile_image('profile_picture.jpg')
            logger.info("Profile picture updated.")
        return None
    except Exception as e:
        logging.debug(e)    

def main():
    try:
        api = config.create_api()
        since_id = config.since_id_read()
        while True:
            check_mentions(api=api, keywords =["ohmyxan_nemesis"], since_id=since_id)
            invert_image(api=api, user='ohmyxan')
            logger.info("Waiting...")
            time.sleep(60)
    except Exception as e:
        config.send_mail_err(str(e))
        logger.error(f"{str(e)}")
        raise e

if __name__ == "__main__":
    main()