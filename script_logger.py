LOG_FILENAME = "activity_log.txt"


def script_log(message):
    with open(LOG_FILENAME, 'at', newline='\n') as f:
        f.write(message)
        f.write("\n")
