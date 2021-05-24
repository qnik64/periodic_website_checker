from datetime import datetime

CACHE_FILENAME = "cached_dates.txt"


def _filter_out_comments(input_list):
    return list(filter(lambda line: line[0] != '#', input_list))


def _gen_comment(list_content):
    length = str(len(list_content)).rjust(2)
    time_stamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return "#new " + length + " entries found on: " + time_stamp + "\n"


def append(list_content):
    with open(CACHE_FILENAME, 'at', newline='\n') as f:
        f.write(_gen_comment(list_content))
        for record in list_content:
            f.write(record)
            f.write("\n")


def read():
    try:
        with open(CACHE_FILENAME, "rt") as f:
            return _filter_out_comments(f.read().split("\n")[:-1])
    except FileNotFoundError:
        return []
