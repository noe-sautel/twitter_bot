# Introduction
Twitter bot is a project started in November 2021 to entertain my best friend on the notorious social network Twitter. Several times a day, he used to tweet for his community but makes some spelling and grammar mistakes, which sometimes, are made with a purpose. When the user @ohmyxan_nemesis is mentionned in a tweet response of @ohmyxan, the bot will collect the text of his tweet, correct it, and then send him a reply with or without correction.

# Description
Below is the description of each file in this repository. Note that by "specific user", I mean the user to correct the tweet for.

.gitignore : Git file to avoid downloading a list of files.
config.py : List the functions to send an email in case of error, to connect to the twitter API with Tweepy, to connect to the textgears API, to read and write the last used tweet id.
licence.txt : Licence file for this program.
main.log : Log file, useful to follow the process or detect errors.
main.py : File allowing to launch the program to correct the tweets of a specific user and to invert the color of the bot's profile image from the specific user.
Procfile : Configuration file for heroku.
profile_picture.jpg : Profile picture of the user.
requirements.text : File allowing to install the libraries required for the good functioning of the program.
since_id.text : File that keeps in memory the identifier of the last tweet read to have a starting base for the program.
textgears.py : Function to connect to the textgears API and clean the text of the tweets and manage the errors.


# How use this project as your own
## Credentials
The program needs credentials to connect to the APIs below. For Twitter, you will find your happiness on https://developer.twitter.com, for textgear https://textgears.com/, smtplib corresponds to the credentials of your mail server.
	Twitter : consumer_key, consumer_secret, access_token, access_token_secret
	textgear : textgear_api
	smtplib : login, password, sender_email, receiver_email
## Procfile
On https://www.heroku.com/, you can host your program and run it. Create an account and then from your dashboard, you will be able to create a pipeline and an application. Don't forget to configure your application so that python is the default language.
## main.py
The main.py file is the heart of the program, you can change the values of the lists "auth_user_list" and "not_follow_self" to change respectively the value of the specific user and the values of the users not to follow: in this case even when wants to correct his own tweet.

There is two main functions for this program.
The first one will retrieve the tweets in which the bot is mentioned, then use textgears.py to clean up the text of the tweet. It will then reply to the user who mentioned it with the appropriate correction. When a user uses the bot to correct a tweet that is not from the specific user, a response in the form of a tweet will be made indicating that it is not possible to make any correction.
The second one will retrieve the image of the specific user, then check if it is different from the one previously saved. If not, then nothing happens; if it is different, the new image is saved, then its colors are reversed to create a cool negative effect before being uploaded as the specific user's profile picture.

When a step is completed, it is automatically recorded in the log file "main.log".

# Ce que je retiens de ce projet
This project allowed me to use again the powers of the Twitter APIs and to better understand their functioning. Moreover, I was able to improve my level in python as well as to take back PEP8 basics and discover the power of linter. Visual Studio Code, then PyCharm, were my IDE for this project, and it was pleasant to discover new features software. Finally, I discovered Heroku as a BAAS (Back-end As A Service) to host and run this program.

For any suggestions, please DM me.