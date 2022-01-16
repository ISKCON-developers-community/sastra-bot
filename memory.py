import redis

memory = redis.Redis(host='localhost', port=6379, db=0)
