import requests
from typing import Tuple, Any

DEFAULT_HEADER = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36")


def similarweb_get(domain: str, headers: list = DEFAULT_HEADER) -> Tuple[Any, Any, Any, Any, Any]:
    endpoint = 'https://data.similarweb.com/api/v1/data?domain=' + domain
    headers = {'User-Agent': headers}

    response = requests.get(url=endpoint, headers=headers)
    if response.status_code == 200:
        r = response.json()
        country = r['CountryRank']['CountryCode']
        rank_local = r['CountryRank']['Rank']
        rank_global = r['GlobalRank']['Rank']
        time_on_site = int(float(r['Engagments']['TimeOnSite'])) if r['Engagments']['TimeOnSite'] != '0' else None
        visits = int(float(r['Engagments']['Visits'])) if r['Engagments']['Visits'] != '0' else None
        return country, rank_local, rank_global, time_on_site, visits
    else:
        print(f'Failed to retrieve data from similarweb: {response.status_code}')
