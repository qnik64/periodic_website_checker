import json
import datetime
import time

import cache
import gmail_interface
import web_grabber

WEEKS_TO_EXAMINE = 30
SEND_TO = "piotr.hoffner.wroc@gmail.com"
LINK_TO_HUMAN_READABLE_WEB = "https://zarejestrowani.pl/w/7i5rOptkNVwJagUP0-PNmcWm-NnFOx0T8vUUHpm3jvvLYbICLoj7if6bHnnn7ffyDRUt3a1zmw_povdsdy2CjA"
LOG_FILENAME = "activity_log.txt"


def script_log(message):
    with open(LOG_FILENAME, 'at', newline='\n') as f:
        f.write(message)
        f.write("\n")


def gen_url(begin_date, end_date):
    base_url = "https://zarejestrowani.pl:8000/api/v1/public/timetable/"
    doctor_hash = "7i5rOptkNVwJagUP0-PNmcWm-NnFOx0T8vUUHpm3jvvLYbICLoj7if6bHnnn7ffyDRUt3a1zmw_povdsdy2CjA"
    response_type = "/?type=1"
    given_dates = "&from_date=" + str(begin_date) + "&to_date=" + str(end_date)
    return base_url + doctor_hash + response_type + given_dates


def send_email_for_dates(found_days):
    subject = "found : " + str(len(found_days)) + " new slots!"
    script_log(subject)
    script_log(', '.join(found_days))
    body = '\n'.join(found_days)
    body += "\nPlease check immediately the website: " + LINK_TO_HUMAN_READABLE_WEB
    gmail_interface.send_email(SEND_TO, subject, body)


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
    new_dates = list_subs(available_dates, cached)
    if len(new_dates):
        send_email_for_dates(new_dates)
        cache.write(available_dates)


start = time.time()
script_log("script started at: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
get_new_dates_for_whole_period()
script_log("script took: " + str(time.time() - start) + "s.")
