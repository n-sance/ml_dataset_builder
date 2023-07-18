import os
import time
import csv
from datetime import datetime
from src.crawlers.an_crawler import save_web_page, get_unique_filename
from src.common.storage_management import pop_new_url, get_size, counter_inc, \
    counter_init, get_counter, add_failed_to_save, size_failed_to_save, pop_new_url_file, get_size_file
from src.common.url_management import parse_url
from src.common.log_management import log, smart_log

WEB_CONTENT_STORAGE = os.getenv('PAGES_SAVER_WEB_CONTENT_STORAGE') or 'web_archive'
REPEAT_HOURS = int(os.getenv('PAGES_SAVER_REPEAT_HOURS')) if os.getenv('PAGES_SAVER_REPEAT_HOURS') else 8
CONTENT_CHUNK_LIMIT = int(os.getenv('PAGES_SAVER_CONTENT_CHUNK_LIMIT')) if os.getenv('PAGES_SAVER_CONTENT_CHUNK_LIMIT') else 5


def append_data_to_csv(data, file_path, header=('phish_url', 'folder', 'target_url')):
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        if not file_exists:
            writer.writerow(header)

        writer.writerow(data)
    log.info(f"Appended to '{file_path}'")


def generate_path(base_path):
    date = datetime.today().strftime("%d_%m_%Y")
    counter = get_counter()
    return os.path.join(base_path, 'webarchive_' + date + '_' + str(counter // CONTENT_CHUNK_LIMIT))


def sharded_safe_url(url, base_path):
    _, netloc, _ = parse_url(url)
    actual_folder = generate_path(base_path)
    url_folder = get_unique_filename(os.path.join(actual_folder, netloc))
    mapping_table = os.path.join(actual_folder, 'mapping.csv')
    if saved := save_web_page(url, url_folder, screenshot=True):
        counter_inc()
        append_data_to_csv((url, url_folder, ''), mapping_table)
        log.info(f'SAVER: {saved} saved: Queue size: {get_size_file()}')
    else:
        add_failed_to_save(url)


def handle_urls():
    try:
        while True:
            q_size = get_size_file()
            if q_size > 0:
                smart_log(f"SAVER: URLs queue size: {q_size}")
                url = pop_new_url_file()
                while url:
                    sharded_safe_url(url, WEB_CONTENT_STORAGE)
                    url = pop_new_url_file()
                smart_log('SAVER: URLs queue is empty')
                log.info(f'SAVER: Failed to save URLs: {size_failed_to_save()}')
            time.sleep(5)
    except Exception as err:
        smart_log(f'SAVER: Oooops... {err}')


if __name__ == '__main__':
    smart_log('SAVER: started')
    handle_urls()
