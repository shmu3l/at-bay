import os
import urllib.request
import urllib.error
from urllib.parse import urlparse


def check_url_status(url_string):

    try:
        proc = os.getpid()
        if not urlparse(url_string).scheme:
            url_string = 'http://' + url_string
            conn = urllib.request.urlopen(url_string)
    except urllib.error.HTTPError as e:
        # Return code error (e.g. 404, 501, ...)
        print(f"[Processed ID: {proc}][] URL STATUS {url_string} : ERROR")
        return "ERROR"
    except urllib.error.URLError as e:
        # Not an HTTP-specific error (e.g. connection refused)
        print(f"[Processed ID: {proc}] URL STATUS {url_string} : INVALID_URL")
        return "INVALID_URL"
    else:
        # 200
        print(f"[Processed ID: {proc}] URL STATUS {url_string} : COMPLETE")
        return "COMPLETE"


if __name__ == "__main__":
    check_url_status()

