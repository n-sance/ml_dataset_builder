from typing import List

from src.common.rest_management import smart_request_simple

RESOURCE = 'https://phishunt.io/feed.txt'


def phishunt_get_resources() -> List[str]:
    response = smart_request_simple(RESOURCE)
    return response.decode('utf-8').split('\n')
