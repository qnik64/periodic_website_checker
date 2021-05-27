import requests
import urllib


import telegram_credentials
from script_logger import script_log


def send_telegram(message):
    url = "https://api.telegram.org/bot"
    url += telegram_credentials.BOT_TOKEN
    url += "/sendMessage?chat_id="
    url += telegram_credentials.CLIENT_CHAT_ID
    url += "&parse_mode=Markdown&text="

    api_req = url + urllib.parse.quote(message)
    response = requests.get(api_req).json()

    if not response['ok']:
        script_log("ERROR! telegram not send")
    if response['ok']:
        script_log("telegram msg send")
