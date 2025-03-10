import redis


def redis_client():
    client = redis.Redis(host='localhost', port=6379, db=0)
    return client
