import time


class RaiTimer:
    def __init__(self, name = ""):
        self.__startTime = time.time()
        self.__name = name

    def __del__(self):
        print(self.__name, " it took: ", time.time() - self.__startTime, "s.")
