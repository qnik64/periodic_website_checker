from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
import datetime
import cache

import gmail_interface

WEEKS_TO_EXAMINE = 30
SEND_TO = "piotr.hoffner.wroc@gmail.com"


def get_json(url):
    try:
        url_response = urlopen(url).read()
        return json.loads(url_response)
    except HTTPError as e:
        if 404 == e.code:
            print(" NOT FOUND: ", url)
        print("An HTTP error occurred on ", url, " error type: ", e)
        return None
    except URLError as e:
        print("An URL error occurred on ", url, " error type: ", e)
        return None


def gen_url(begin_date, end_date):
    base_url = "https://zarejestrowani.pl:8000/api/v1/public/timetable/"
    doctor_hash = "7i5rOptkNVwJagUP0-PNmcWm-NnFOx0T8vUUHpm3jvvLYbICLoj7if6bHnnn7ffyDRUt3a1zmw_povdsdy2CjA"
    response_type = "/?type=1"
    given_dates = "&from_date=" + str(begin_date) + "&to_date=" + str(end_date)
    return base_url + doctor_hash + response_type + given_dates


def send_email_for_dates(found_days):
    subject = "found : " + str(len(found_days)) + " new slots!"
    print(subject)
    body = ''
    for day in found_days:
        body += str(day)
        body += '\n'
    gmail_interface.send_email(SEND_TO, subject, body)


def examine_one_week(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    response = get_json(gen_url(start_date, end_date))
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
        cache.append(new_dates)


get_new_dates_for_whole_period()
