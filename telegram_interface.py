import requests

import telegram_credentials


def send_telegram(message):
    url = "https://api.telegram.org/bot"
    url += telegram_credentials.BOT_TOKEN
    url += "/sendMessage?chat_id="
    url += telegram_credentials.CLIENT_CHAT_ID
    url += "&parse_mode=Markdown&text="

    response = requests.get(url + message)
    return response.json()
