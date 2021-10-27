from pprint import pprint
from pymongo import MongoClient
import json
import os
import pandas as pd
import requests
import twython

# Get twitter and mongoDB credentials
with open('credentials.json') as json_file:
    # https://developer.twitter.com/en/portal/dashboard
    creds = json.load(json_file)

twitter = twython.Twython(creds['api_key'], creds['api_secret_key'], creds['bearer_token'])

query = "from:950noah -is:retweet"
# query = "from:noesautel -is:retweet"

# Fields docs : https://developer.twitter.com/en/docs/twitter-api/fields
# # Options include: attachments, author_id, context_annotations, conversation_id, created_at, entities, geo, id, in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
# possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets, source, text, and withheld

tweet_fields = "tweet.fields=author_id,public_metrics,geo,created_at"
url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(query, tweet_fields)

response = requests.request("GET", url, headers={"Authorization": "Bearer {}".format(creds['bearer_token'])})
print(response.json())

# MongoDB
logins = [creds['mdb_id'], creds['mdb_pass']]
client = MongoClient("mongodb+srv://{}:{}@cluster0.lachp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(*logins))


db = client.twitter_bot
# Create collection orginalTweet
orginalTweet = db.orginalTweet

orginalTweetDocument = response.json()
orginalTweet.insert_one(orginalTweetDocument)
print('Tweet has beeen inserted.')