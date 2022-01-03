from datetime import time
from os import environ
import logging
import smtplib
import ssl
import tweepy
import time

logger = logging.getLogger()


def send_mail_err(error_content):
    # Create a secure SSL context
    context = ssl.create_default_context()
    port = 465
    login = environ.get("gmail_log")
    password = environ.get("gmail_pass")

    sender_email = environ.get("gmail_log")
    receiver_email = environ.get("icloud_log")
    message = f"""Subject: Heroku : twitter-bot-ohmyxan error

    Une erreur a été detecté pour @ohmyxan_nemesis.

    Heroku: https://dashboard.heroku.com/apps/twitter-bot-ohmyxan/resources
    Twitter : https://twitter.com/ohmyxan_nemesis

    Détails de l'erreur
    ---
    {error_content}
    ---
    """.encode(
        "utf-8"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message)

    logger.info("Email error sent")


def create_api():
    consumer_key = environ.get("api_key")  # CONSUMER_KEY
    consumer_secret = environ.get("api_secret_key")  # CONSUMER_SECRET
    access_token = environ.get("acess_token")
    access_token_secret = environ.get("acess_token_secret")

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
        return environ.get("textgears_api_key")
    except Exception as e:
        logger.error("Error getting Textgears API", exc_info=True)
        raise e


def since_id_read():
    with open("since_id.text", "r") as fp:
        return int(fp.read())


def since_id_write(current_since_id):
    with open("since_id.text", "w") as fp:
        fp.write(str(current_since_id))


def time_sleep(my_function, seconds):
    time.sleep(seconds)
    return my_function