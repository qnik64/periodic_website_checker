import time
from script_logger import script_log
from datetime import datetime


def get_date_and_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class RaiTimer:
    def __init__(self, name=""):
        self.__startTime = time.time()
        self.__name = name

    def __del__(self):
        time_in_sec = time.time() - self.__startTime
        script_log("and took: " + f'{time_in_sec:.3f}' + "s.")
