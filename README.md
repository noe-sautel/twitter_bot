# Présentation et motivation
Twitter bot est un projet réalisé entre novembre et décembre 2021 pour divertir, amuser et conseiller mon ami Zak. Plusieurs fois par jour, il a l'habitue de tweeter pour sa communauté mais fait quelques fautes d'orthographe et de grammaire, qui parfois, sont volontaires. L'utilisateur @ohmyxan_nemesis, lorsqu'il est tagué sur un tweet de @ohmyxan, collectera le texte de son tweet, le corrigera, puis lui enverra une réponse avec ou sans correction.

# Description
Ci-dessous la description de chaque fihciers de ce repositery. A noter que par "utilisateur spécifique", j'entends mon ami Zak, soit l'utilisateur pour lequel on souhaite corriger le text des tweets.

.gitignore : Fichier git permettant de ne pas télécharger des fichiers privés sur ce repository
config.py : Recence les fonctions pour envoyer un email en cas d'erreur, se connecter à l'API twitter avec Tweepy, se connecter à l'API textgears, de lecture et écriture du dernier id tweet utilisé
licence.txt : Fichier de licence pour ce programme
main.log : Fichier de log, utile pour suivre le processus ou détecter des erreurs
main.py : Fichier permettant de lancer le programme pour corriger les tweets d'un utilisateur spécifique et inverser la couleur de l'image de profil du bot issue de l'utilisateur spécifique
Procfile : Fichier de configuration pour heroku
profile_picture.jpg : Photo de profil de l'utilisateur
requirements.text : Fichier permettant d'installer les librairies requises au bon fonctionnement du programme
since_id.text : Fichier qui garde en mémoire l'identifiant du dernier tweet lu permettant d'avoir une base de départ pour le programme
textgears.py : Fonction pour se connecter à l'API de textgears et nettoyer le text des tweets et gérer les erreurs. 


# How use this project as your own
## Credentials
Le programme a besoin des credentiales pour se connecter aux APIs ci-dessous. Pour Twitter, vous trouverez votre bonheur sur https://developer.twitter.com, pour textgear https://textgears.com/, smtplib correspond aux identifiants de votre serveur de messagerie. 
	Twitter : consumer_key, consumer_secret, access_token, access_token_secret
	textgear : textgear_api
	smtplib : login, password, sender_email, receiver_email
## Procfile
Sur https://www.heroku.com/, vous pouvez héberger votre programme et le faire fonctionner. Pour cela, créer un compte puis depuis votre dashborad, vous aurez la possibilité de créer une pipeline puis une application. N'oubliez pas de configurer votre application afin que python soit le language utilisée par défaut.
## main.py
Le fichier main.py est le coeur du programme, vous pouvez changer les valeurs des listes "auth_user_list" et "not_follow_self" pour changer respectivement la valeur de l'utilisateur spécifique et les les valeurs des utilisateurs à ne pas follow : en l'occurence soit même lorsque souhaite corriger son propre tweet.

Le programme fonctionne en multithreatdeading. 
Le premier permet d'aller récupérer les tweets dans lesquels le bot est mentionné, puis utilisera textgears.py pour nettoyer le texte du tweet. Il répondra ensuite à l'utilisateur qui l'a mentionné avec la correction appropriée. Lorsqu'un utilisateur utilise le bot pour corriger un tweet n'émanant pas de l'utilisateur spécifique, une réponse sous forme de tweet sera apporté indiquant qu'il n'est pas possible d'apporter une quelconque correction.
Le second va récupérer l'image de l'utilisateur spécifique, puis vérifie si celle-ci diffère de celle précédement enregistrée. Si ce n'est pas le cas, alors rien ne se passe ; si elle est différente, la nouvelle image est enregistré, puis ses couleurs sont inversés pour créer un effet négatif froid avant d'être téléchargé en tant que photo de profil de l'utilisateur spécifique.

Lorsque qu'une étape est complété, celle-ci est automatiquement enregistré dans le fichier de logs "main.log".

# Ce que je retiens de ce projet
Ce projet m'a permis de réutiliser à nouveau les pouvoirs des APIs twitter et de mieux appréhender leurs fonctionnemnts. De plus, j'ai pu perfectionner mon niveau en python ainsi que reprendre des bases PEP8 et découvrir la puissance des linter. Visual Studio Code a été mon IDE pour ce projet et j'ai été très satisfait de découvrir les fonctionnalités de ce logiciel. Enfin, j'ai découvert Heroku en tant que BAAS (Back-end As A Service) pour héberger et faire fonctionner ce programme.

Pour toutes suggestions vous pouvez me DM.