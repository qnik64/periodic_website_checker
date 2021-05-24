from urllib.request import urlopen
from urllib.error import HTTPError, URLError


def get_site(url):
    try:
        return urlopen(url).read()
    except HTTPError as e:
        if 404 == e.code:
            print(" NOT FOUND: ", url)
        print("An HTTP error occurred on ", url, " error type: ", e)
        return None
    except URLError as e:
        print("An URL error occurred on ", url, " error type: ", e)
        return None
