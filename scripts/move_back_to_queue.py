from src.common.storage_management import get_records, remove_records, get_size, save_url
from src.common.log_management import log


NUMBER = 100

if __name__ == '__main__':
    log.info(f"MOVER: started. Queue size: {get_size('urls_queue')}. "
           f"Target number of records: {NUMBER}")
    records = get_records('urls_set', NUMBER)
    if records:
        for rec in records:
            save_url(rec)
    log.info(f"MOVER: Reverting to queue completed. Queue size: {get_size('urls_queue')}. ")
