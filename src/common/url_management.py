from typing import Tuple
from urllib.parse import urlparse


def autocomplete_scheme(url: str, scheme='http') -> str:
    if not url.startswith('http'):
        return scheme + '://' + url
    return url


def parse_url(url: str) -> Tuple[str, str, str]:
    parsed = urlparse(url)
    scheme = parsed.scheme

    if not scheme:
        # If the scheme is missing, assume it as 'http'
        modified_url = 'http://' + url
        parsed = urlparse(modified_url)

    netloc = parsed.netloc.replace('www.', '')
    path_n_params = ''.join((parsed.path, '?', parsed.query, parsed.params))
    return scheme, netloc, path_n_params
