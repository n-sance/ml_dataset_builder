import os
import schedule
import time

from src.crawlers.an_crawler import save_web_page, get_unique_filename
from src.common.storage_management import pop_new_url, get_size
from src.common.url_management import parse_url
from src.common.log_management import log, smart_log

WEB_CONTENT_STORAGE = os.getenv('PAGES_SAVER_WEB_CONTENT_STORAGE') or 'web_archive'
REPEAT_HOURS = int(os.getenv('PAGES_SAVER_REPEAT_HOURS')) if os.getenv('PAGES_SAVER_REPEAT_HOURS') else 8


def handle_urls():
    smart_log(f"SAVER: URLs queue size: {get_size()}")
    url = pop_new_url()

    while url:
        _, netloc, _ = parse_url(url)

        if saved := save_web_page(url, os.path.join(WEB_CONTENT_STORAGE, get_unique_filename(netloc)), screenshot=True):
            log.info(f'SAVER: {saved} saved')
        url = pop_new_url()
    smart_log('SAVER: URLs queue is empty')


if __name__ == '__main__':
    smart_log('SAVER: started')
    handle_urls()
    schedule.every(REPEAT_HOURS).hours.do(handle_urls)

    while True:
        schedule.run_pending()
        time.sleep(1)
