import asyncio
import schedule
import time
import os
from src.resources_collect.tweetfeed import tweetfeed_get_resources
from src.resources_collect.openphish import openphish_get_resources
from src.resources_collect.phishstats import phishstats_get_resources
from src.resources_collect.phishunt import phishunt_get_resources
from src.resources_collect.phishingarmy import phishingarmy_get_resources
from src.common.storage_management import is_new, save_url, get_size
from src.common.log_management import smart_log, log
from src.common.rest_management import check_urls


REPEAT_HOURS = int(os.getenv('URL_GRABBER_REPEAT_HOURS'))


def main():
    smart_log('URL GRABBER: Service started')
    smart_log(f"URL GRABBER: URLs queue size: {get_size('urls_queue')}")

    tweetfeed = tweetfeed_get_resources('today')

    openphish = openphish_get_resources()

    phishstats = phishstats_get_resources()

    phishunt = phishunt_get_resources()

    # phisharmy = phishingarmy_get_resources()

    smart_log(f'URL GRABBER: Phisharmy: received {0} urls\nPhishunt: received {len(phishunt)} urls\nPhishstats: received {len(phishstats)} urls\nOpenphish: received {len(openphish)} urls\nTweetfeed: received {len(tweetfeed)} urls')

    total = set(tweetfeed).union(set(openphish), set(phishstats), set(phishunt))
    unique_total = []
    for url in total:
        if is_new(url):
            unique_total.append(url)
    log.info(f'URL GRABBER: NEW URLs {unique_total}')
    smart_log(f'URL GRABBER: Total: received {len(total)}, unique: {len(unique_total)} urls')

    alive_unique_total = asyncio.run(check_urls(unique_total))
    alive_unique_total = [v for v in alive_unique_total if v is not None]

    for url in alive_unique_total:
        save_url(url)

    dead = [v for v in unique_total if v not in alive_unique_total]

    log.info(f'URL GRABBER: Alive unique: {alive_unique_total}')
    log.info(f'URL GRABBER: Dead: {dead}')
    smart_log(f'URL GRABBER: {len(alive_unique_total)} alive unique URLs were added to storage. Dead URLs: {len(dead)}')
    smart_log(f"URL GRABBER: URLs queue size: {get_size('urls_queue')}")


if __name__ == '__main__':
    main()
    schedule.every(REPEAT_HOURS).hours.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
