import os
import redis
import queue

q = queue.Queue()

with open('urls.txt', 'r') as f:
    lines = f.readlines()

    for l in lines:
        q.put(l.strip())

host = os.getenv('REDIS_HOST') or 'localhost'
port = int(os.getenv('REDIS_PORT')) if os.getenv('REDIS_PORT') else 6379


r = redis.Redis(host=host, port=port, db=0)
r.ping()

r.expire('notifications_queue', 3600)
r.expire('urls_queue', 3600)


def is_new(url):
    if not r.sismember('urls_set', url):
        return True


def get_size(name='urls_queue'):
    size = r.llen(name)
    return size


def get_size_file():
    return q.qsize()


def save_url(url):
    r.sadd('urls_set', url)
    r.lpush('urls_queue', url)
    return True


def pop_new_url() -> str:
    url = r.rpop('urls_queue')
    if url:
        return url.decode('utf-8')


def pop_new_url_file() -> str:
    if not q.empty():
        return q.get()

def add_message(msg: str):
    return r.lpush('notifications_queue', msg)


def pop_message():
    return r.rpop('notifications_queue')


def get_counter():
    c = r.get('counter')
    if not c:
        counter_init()
    return int(c.decode('utf-8')) if c else 0


def counter_init():
    return r.set('counter', 0)


def counter_inc():
    return r.incr('counter')


def add_failed_to_save(url):
    r.sadd('failed_set', url)


def size_failed_to_save():
    return r.scard('failed_set')


def get_records(redis_key: str, count: int) -> list:
    return r.srandmember(redis_key, count)


def get_all_records(redis_key: str):
    return [x.decode('utf-8') for x in r.smembers(redis_key)]

def get_instance():
    return r

def remove_records(redis_key: str, records: list):
    return r.srem(redis_key, *records)
