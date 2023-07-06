import schedule
import time
from src.common.log_management import pop_message, tg_send, smart_log, log
POLL_TIMEOUT = 5


def action():
    try:
        msg = pop_message()
        if msg:
            tg_send(msg.decode('utf-8'))
    except Exception as err:
        log.error(f'NOTIFICATOR: {err}')


if __name__ == '__main__':
    smart_log('NOTIFICATOR: started')
    action()
    schedule.every(POLL_TIMEOUT).seconds.do(action)

    while True:
        schedule.run_pending()
        time.sleep(1)
