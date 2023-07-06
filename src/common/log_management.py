import logging
import sys
import os
import requests
from src.common.storage_management import add_message, pop_message


token = os.getenv('LOG_BOT_TOKEN')
chat_id = os.getenv('LOG_CHAT_ID')
logfile = os.getenv('LOG_LOGFILE_PATH')


class Logger:
    def __init__(self, log_file):
        self.log_format = "%(asctime)s [%(levelname)s] %(message)s"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


logger = Logger(logfile)
log = logger.get_logger()


def tg_send(text: str):
    try:
        q = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={text}'
        requests.get(q)
    except Exception as err:
        log.info(f'TG sending problem: {err}')


def tg_log(text: str):
    add_message(text)

def smart_log(text: str):
    log.info(text)
    tg_log(text)
