from typing import List

from src.common.rest_management import smart_request_simple

RESOURCE = 'https://api.tweetfeed.live/v1/{period}/phishing/url'


def tweetfeed_get_resources(period: str) -> List[str]:
    """
    :param period: today, week, month, year
    """
    return [url['value'] for url in smart_request_simple(RESOURCE.format(period=period))]
