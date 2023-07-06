from typing import List

from src.common.rest_management import smart_request_simple

RESOURCE = 'https://openphish.com/feed.txt'


def openphish_get_resources() -> List[str]:
    try:
        a = smart_request_simple(RESOURCE)
        return a.decode('utf-8').split('\n')
    except Exception as err:
        print(f'Error during retrieveing info from openphish: {err}')