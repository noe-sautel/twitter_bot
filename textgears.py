# import demjson
import json
import requests
import urllib.parse
import emoji


def correct_text(tweet_text, api_key):

    safe_string = urllib.parse.quote_plus(tweet_text, safe="'")
    r = requests.get(
        "https://api.textgears.com/grammar?text="
        + safe_string
        + "&language=fr-FR&whitelist=&dictionary_id=&key="
        + api_key
    )
    pretty_json = json.loads(r.text)
    # data = json.dumps(pretty_json, indent=2)
    # # print(data)
    # pretty_json = demjson.decode(data)

    try:
        if not pretty_json["response"]["errors"]:
            return (
                f"Aucune erreur trouvée. Si il y'en a une, vous pouvez"
                f" me DM : @noesautel "
                f"{emoji.emojize(':technologist_medium_skin_tone:')}"
            )
        else:
            description = pretty_json["response"]["errors"][0]["description"]["en"]
            better = pretty_json["response"]["errors"][0]["better"][0]
            return f"""{description} {emoji.emojize(':right_arrow:')} \"{better}\""""
    except Exception as e:
        return str(e)
