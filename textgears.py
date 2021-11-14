import demjson
import emoji
import json
import requests
import urllib.parse

def correct_text(tweet_text, user_tweet_name, api_key):

    safe_string = urllib.parse.quote_plus(tweet_text, safe="'")
    r = requests.get('https://api.textgears.com/grammar?text='+safe_string+'&language=fr-FR&whitelist=&dictionary_id=&key='+api_key) 
    pretty_json = json.loads(r.text)
    data = json.dumps(pretty_json, indent=2)    
    py_obj = demjson.decode(data)

    try:
        if not py_obj["response"]["errors"]:
            return "Aucune erreur trouvée. Si il y'en a une, vous pouvez me DM : @" + str(user_tweet_name) + emoji.emojize(":thumbs_up:")
        else:
            description = py_obj["response"]["errors"][0]["description"]["en"]
            better = py_obj["response"]["errors"][0]["better"][0]
            # return {"description": description, "better": better}
            return f"{description} \"{better}\" " # + {emoji.emojize(":thumbs_up:")}
    except Exception as e:
        return str(e)

# r = requests.get('https://api.textgears.com/account/resourcequota?key='+api_key) 
# file = 'data.txt'
# with open('data.txt', 'w') as outfile:
#     json.dump(data, outfile)
# with open(file, 'r') as f:
#     data = json.load(f)