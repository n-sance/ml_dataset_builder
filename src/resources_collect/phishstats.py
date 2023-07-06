from typing import List

from src.common.rest_management import smart_request_simple

RESOURCE = 'https://phishstats.info:2096/api/phishing?_sort=-date'


def phishstats_get_resources() -> List[str]:
    return [url['url'] for url in smart_request_simple(RESOURCE)]
