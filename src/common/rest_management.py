import json
import aiohttp
import asyncio
import requests
from requests import RequestException
from typing import Union
from src.common.url_management import parse_url
from src.common.log_management import log

requests.packages.urllib3.disable_warnings()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}


def smart_request_simple(url: str, enable_headers: bool = False) -> Union[dict, bytes]:
    scheme, netloc, path_n_params = parse_url(url)
    try:
        response = smart_request(netloc, path_n_params, scheme, enable_headers)
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.content
        response.raise_for_status()
    except Exception as err:
        print(f'Failed to retrieve data from {scheme}: {err}')


def smart_request(netloc: str, path_n_params: str = '', scheme: str = '', enable_headers: bool = True) -> requests.Response:
    uri = ''.join([netloc, path_n_params])
    headers = HEADERS if enable_headers is True else {}

    try:
        if scheme:
            query = scheme + '://' + uri
        else:
            query = 'https://' + uri

        response = requests.get(query, headers=headers, verify=False)
        return response

    except RequestException as err:
        if scheme == 'http':
            log.error(f'http error for url: {uri} -> {err}')
        else:
            log.warning(f'{scheme} error for url {uri}: {err}, trying http')
            smart_request(netloc, path_n_params, 'http', enable_headers)


async def is_page_alive(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url, timeout=5, headers=HEADERS, verify_ssl=False) as response:
                return url if 200 <= response.status <= 399 else None
        except Exception as err:
            log.warning(f'Is page alive error: {err}')
            return None


def is_page_alive_sync(url):
    try:
        response = requests.get(url, timeout=5, headers=HEADERS)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


async def check_urls(urls, batch_size=20):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=batch_size)) as session:
        semaphore = asyncio.Semaphore(batch_size)
        tasks = []

        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i : i + batch_size]
            batch_tasks = [
                is_page_alive(session, url, semaphore)
                for url in batch_urls
            ]
            tasks.extend(batch_tasks)

        return await asyncio.gather(*tasks)
