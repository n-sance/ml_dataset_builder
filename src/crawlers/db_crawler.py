import scrapy
from pathlib import Path
from urllib.parse import urlparse
from common.url_management import autocomplete_scheme
from common.files_management import read_urls


class HomepageSpider(scrapy.Spider):
    name = "homepage_spider"

    def start_requests(self):

        original_domains = read_urls(Path('input.txt'))
        original_domains = [autocomplete_scheme(domain, 'http') for domain in original_domains]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "DNT": "1",
            "Referer": "https://www.google.com/",
            "Upgrade-Insecure-Requests": "1",
        }

        for url in original_domains:
            yield scrapy.Request(url=url, callback=self.parse, headers=headers)

    def parse(self, response, **kwargs):
        filename = f"html_files/{urlparse(response.url).netloc.replace('www.', '')}.html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
        'DOWNLOAD_TIMEOUT': 30,
        'DOWNLOAD_DELAY': 5,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }