import os
import redis


host = os.getenv('REDIS_HOST')
port = int(os.getenv('REDIS_PORT')) if os.getenv('REDIS_PORT') else 6379

r = redis.Redis(host=host, port=port, db=0)
r.ping()
r.expire('notifications_queue', 3600)


def is_new(url):
    if not r.sismember('urls_set', url):
        return True


def get_size(name='urls_queue'):
    size = r.llen(name)
    return size


def save_url(url):
    r.sadd('urls_set', url)
    r.lpush('urls_queue', url)
    return True


def pop_new_url() -> str:
    url = r.rpop('urls_queue')
    if url:
        return url.decode('utf-8')


def add_message(msg: str):
    return r.lpush('notifications_queue', msg)


def pop_message():
    return r.rpop('notifications_queue')