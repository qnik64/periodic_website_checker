from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import json
import datetime

WEEKS_TO_EXAMINE = 26


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


def examine_one_week(start_date):
    end_date = start_date + datetime.timedelta(days=6)
    response = get_json(gen_url(start_date, end_date))
    dates = json.loads(response['days'])
    print("found : ", len(dates), " slots between ", start_date, " and ", end_date)
    for day in dates:
        print(day)


today = datetime.date.today()
for i in range(WEEKS_TO_EXAMINE):
    examine_one_week(today + datetime.timedelta(days=i * 7))
