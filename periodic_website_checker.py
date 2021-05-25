import json
import datetime
import urllib


import cache
import gmail_interface
import telegram_interface
import web_grabber
from updater import git_update
from script_logger import script_log
from timer import RaiTimer, get_date_and_time


WEEKS_TO_EXAMINE = 10
SEND_TO = "piotr.hoffner.wroc@gmail.com"
LINK_TO_HUMAN_READABLE_WEB = "https://zarejestrowani.pl/w/7i5rOptkNVwJagUP0-PNmcWm-NnFOx0T8vUUHpm3jvvLYbICLoj7if6bHnnn7ffyDRUt3a1zmw%5Fpovdsdy2CjA"


def gen_url(begin_date, end_date):
    base_url = "https://zarejestrowani.pl:8000/api/v1/public/timetable/"
    doctor_hash = "7i5rOptkNVwJagUP0-PNmcWm-NnFOx0T8vUUHpm3jvvLYbICLoj7if6bHnnn7ffyDRUt3a1zmw_povdsdy2CjA"
    response_type = "/?type=1"
    given_dates = "&from_date=" + str(begin_date) + "&to_date=" + str(end_date)
    return base_url + doctor_hash + response_type + given_dates


def send_nofifications_for_dates(found_days):
    subject = "[zarejestrowani alert] found : " + str(len(found_days)) + " new slots!"
    script_log(subject + " @ " + ', '.join(found_days))
    found_dates = '\n'.join(found_days)
    action = "\nPlease check immediately the website: " \

    body = found_dates + action + LINK_TO_HUMAN_READABLE_WEB
    gmail_interface.send_email(SEND_TO, subject, body)

    telegram_interface.send_telegram(subject)
    telegram_interface.send_telegram(found_dates)
    telegram_interface.send_telegram(action + urllib.parse.quote(LINK_TO_HUMAN_READABLE_WEB))


def examine_one_week(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    url = gen_url(start_date, end_date)
    response = json.loads(web_grabber.get_site(url))
    return json.loads(response['days'])


def get_dates_for_whole_period():
    today = datetime.date.today()
    dates = []
    for i in range(WEEKS_TO_EXAMINE):
        dates.extend(examine_one_week(today + datetime.timedelta(days=i * 7)))
    return dates


def list_subs(subtrahend, minuend):
    return sorted([item for item in subtrahend if item not in minuend])


def get_new_dates_for_whole_period():
    cached = cache.read()
    available_dates = get_dates_for_whole_period()
    script_log(str(len(available_dates)) + " slots foud " + ', '.join(available_dates))
    new_dates = list_subs(available_dates, cached)
    if len(new_dates):
        send_nofifications_for_dates(new_dates)
        cache.write(available_dates)


def periodic_website_checker():
    timer = RaiTimer()
    git_update()
    script_log("started at: " + get_date_and_time())
    get_new_dates_for_whole_period()


periodic_website_checker()
