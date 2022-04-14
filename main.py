import tweepy
import logging
import emoji

# import config_creds as config

import config
import time
import textgears
import re
from PIL import Image, ImageChops
import requests
from io import BytesIO

# TODO: add threading for the img w/ an upd a day
# TODO: check if possible to have two threads w/
#       a while loop for check_mentions and invert_image
# TODO: update the bio with current bot status
# todo reconfig hook for pre commit
# TODO: shut down the bot if an error occurred

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()],
)
logger = logging.getLogger()

user_list_to_correct = ["ohmyxan"]
not_follow_self = ["ohmyxan_nemesis"]


def check_mentions(api, keywords, since_id):
    """
    Listen for mentions and keywords to activate the bot.
    Args:
        api: Twitter api made with config.create_api()
        keywords: Words to listen for bot activation
        since_id: Last id collected with config.since_id_read()

    Returns: Send a response via the api and update since_id.text file.

    """
    new_since_id = config.since_id_read()
    logger.info(f"Retrieving mentions with since id: {new_since_id}")

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        logging.info(
            f"""CURSOR: [since_id]:{since_id}; [tweet.id]:{tweet.id}; [text]:{tweet.text}; [user.name]:{tweet.user.name}; [in_reply_to_status_id]:{tweet.in_reply_to_status_id}"""
        )

        try:
            api.get_status(tweet.in_reply_to_status_id)
        except tweepy.errors.HTTPException as error:
            if error.api_codes in [[144], [8]]:
                # Exception raised when an HTTP request fails
                continue
            else:
                raise error

        if not tweet.in_reply_to_status_id:
            # when it is not in a reply, continue
            continue
        elif api.get_status(
            tweet.in_reply_to_status_id
        ).user.screen_name not in user_list_to_correct and any(
            keyword in tweet.text for keyword in keywords
        ):
            try:
                api.update_status(
                    status=f"Désolé, mais je ne corrige que les tweets de "
                    f"@ohmyxan {emoji.emojize(':blue_heart:')} Et je "
                    f"ne le fais qu'une seule fois par thread.",
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                )
                logger.info(
                    f"Answered to {tweet.user.name} on {tweet.id} with @ohmyxan filter"
                )
            except tweepy.errors.HTTPException as error:
                if error.api_codes != [187]:
                    raise error
                logger.warning(f"Duplicate tweet {tweet.id}.")
                continue
        elif (
            api.get_status(tweet.in_reply_to_status_id).user.screen_name
            in user_list_to_correct
            and any(keyword in tweet.text for keyword in keywords)
            and api.get_status(tweet.in_reply_to_status_id).user.screen_name
            not in not_follow_self
        ):
            tweet_typo_prepared = api.get_status(tweet.in_reply_to_status_id).text
            tweet_typo = " ".join(
                re.sub(
                    "(@[A-Za-z0-9_À-ÿ]+)|([^0-9A-Za-z_À-ÿ \t])|(\w+:\/\/\S+)",
                    " ",
                    tweet_typo_prepared,
                ).split()
            )
            tweet_corrected = textgears.correct_text(
                tweet_text=tweet_typo, api_key=config.textgears_api()
            )
            try:
                api.update_status(
                    status=tweet_corrected,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True,
                )
                logger.info(
                    f"Answered to {tweet.user.name} "
                    f"on {tweet.id}: {tweet_corrected}."
                )
            except tweepy.errors.HTTPException as error:
                if error.api_codes != [187]:
                    raise error
                logger.warning(f"Duplicate tweet {tweet.id}")
                continue
        else:
            # continue
            return new_since_id
        if not tweet.user.following and tweet.user.screen_name not in not_follow_self:
            tweet.user.follow()
            logger.info(f"User @{tweet.user.name} has just been followed")

        config.since_id_write(current_since_id=new_since_id)
        return new_since_id


def invert_image(api, user):
    try:
        lookup_user = api.lookup_users(screen_name=[user])[0]
        img_raw = "".join(
            re.sub("_normal", " ", lookup_user.profile_image_url_https).split()
        )  # withdraw "_normal" get a 400*400px img instead of miniature
        response = requests.get(img_raw)
        img = Image.open(BytesIO(response.content))
        inv_img = ImageChops.invert(img)
        im1 = Image.open("profile_picture.jpg")
        inv_img.save("profile_picture.jpg")
        im2 = Image.open("profile_picture.jpg")
        if list(im1.getdata()) == list(im2.getdata()):
            logger.info("Profile picture identical ; no update.")
        else:
            api.update_profile_image("profile_picture.jpg")
            logger.info("Profile picture updated.")
        return None
    except Exception as e:
        logging.debug(e)


def main():
    try:
        api = config.create_api()
        since_id = config.since_id_read()
        while True:
            # threading.Thread
            # (target=check_mentions(api=api, keywords =["grammaire"],
            # since_id=since_id)).start()
            # threading.Thread(
            #     target=check_mentions(
            #         api=api, keywords=["grammaire"], since_id=since_id
            #     )
            # ).start()
            # threading.Thread(target=invert_image(api=api, user="ohmyxan")).start()
            try:
                check_mentions(api=api, keywords=["grammaire"], since_id=since_id)
                invert_image(api=api, user="ohmyxan")
                logger.info("Waiting...")
                time.sleep(60)
            except tweepy.errors.HTTPException as error:
                if error.api_codes != [404]:
                    config.send_mail_err(error_content=str(error))
                    continue

    except Exception as e:
        config.send_mail_err(error_content=str(e))
        logger.error(f"{str(e)}")
        raise e


if __name__ == "__main__":
    main()
