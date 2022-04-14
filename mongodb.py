from pymongo import MongoClient
from pprint import pprint

# db=client.admin
logins = ["noestl", "agora"]
client = MongoClient(
    "mongodb+srv://{}:{}@cluster0.lachp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
        *logins
    )
)

db = client.test
# Issue the serverStatus command and print the results
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)


# db = client.twitter_bot
# Create collection answer
# answer = db.answer

# import datetime
# personDocument = {
#   "name": { "first": "Alan", "last": "Turing" },
#   "birth": datetime.datetime(1912, 6, 23),
#   "death": datetime.datetime(1954, 6, 7),
#   "contribs": [ "Turing machine", "Turing test", "Turingery" ],
#   "views": 1250000
# }

# answer.insert_one(personDocument)

# print(answer.find_one({ "name.last": "Turing" }))
