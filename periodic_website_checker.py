from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
import datetime

import gmail_interface

WEEKS_TO_EXAMINE = 27
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


def send_email_for_dates(start_date, end_date, found_days):
    subject = "found : " + str(len(found_days)) + " slots between " + str(start_date) + " and " + str(end_date)
    print(subject)
    body = ''
    for day in found_days:
        body += str(day)
        body += '\n'
    gmail_interface.send_email(SEND_TO, subject, body)


def examine_one_week(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    response = get_json(gen_url(start_date, end_date))
    dates = json.loads(response['days'])
    if len(dates):
        send_email_for_dates(start_date, end_date, dates)


today = datetime.date.today()
for i in range(WEEKS_TO_EXAMINE):
    examine_one_week(today + datetime.timedelta(days=i * 7))
