# import demjson
import json
import requests
import urllib.parse
import emoji
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("main.log"), logging.StreamHandler()],
)
logger = logging.getLogger()


def correct_text(tweet_text, api_key):

    safe_string = urllib.parse.quote_plus(tweet_text, safe="'")
    r = requests.get(
        "https://api.textgears.com/grammar?text="
        + safe_string
        + "&language=fr-FR&whitelist=&dictionary_id=&key="
        + api_key
    )
    pretty_json = json.loads(r.text)

    try:
        if pretty_json["error_code"] == 607:
            # Lack of credits
            logger.warning(
                f"""textgears.correct_text error_code: {pretty_json["error_code"]} description: {pretty_json["description"]}"""
            )
            return f"Je n'ai plus de crédits pour accéder à mon dictionnaire. Essaie une autre fois ou contacte @noesautel {emoji.emojize(':technologist_medium_skin_tone:')}"
            return None
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
        logger.warning(f"textgears.correct_text error: {e}")
