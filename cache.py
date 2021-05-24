from datetime import datetime
import json

CACHE_FILENAME = "cached_dates.json"


def write(list_content):
    with open(CACHE_FILENAME, 'wt') as f:
        f.write(json.dumps(list_content))
        f.write("\n")


def read():
    try:
        with open(CACHE_FILENAME, "rt") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return []
