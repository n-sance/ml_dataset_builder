from typing import List

from src.common.rest_management import smart_request_simple

RESOURCE = 'https://phishing.army/download/phishing_army_blocklist.txt'


def phishingarmy_get_resources() -> List[str]:
    response = smart_request_simple(RESOURCE)
    response = response.decode('utf-8').split('\n')
    response = [r for r in response if not r.startswith('#')]
    return response
