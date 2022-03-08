import json
import logging
import smtplib
import ssl

# import tweepy

logger = logging.getLogger()

with open("credentials.json") as json_file:
    creds = json.load(json_file)


def send_mail_err(error_content):
    # Create a secure SSL context
    context = ssl.create_default_context()
    port = 465  # For SSL
    login = creds["gmail_log"]
    password = creds["gmail_pass"]
    sender_email = creds["gmail_log"]
    receiver_email = creds["icloud_log"]
    message = "Subject: Heroku : twitter-bot-ohmyxan error"


gmail_user = creds["gmail_log"]
gmail_password = creds["gmail_pass"]

sent_from = gmail_user
to = creds["icloud_log"]
subject = "OMG Super Important Message"
body = "Hey, what"

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (
    sent_from,
    ", ".join(to),
    subject,
    body,
)
# p3LHLr2ujmxi
try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    print([gmail_user, gmail_password])
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()
    print("Email sent")
except Exception as error:
    print(error)
    print("Something went wrong...")
