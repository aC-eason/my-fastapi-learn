import json

import redis

from config.config import RedisConfig as redis_config

r = redis.Redis()

class Redis:
    def __init__(self, key_prefix='', expire_time=0):
        self.config = redis_config
        self.redis_client = redis.Redis(
            host=self.config.HOST, port=self.config.PORT, db=self.config.DB, password=self.config.PASSWORD,
            encoding="utf-8", decode_responses=True)
        self.key_prefix = key_prefix
        self.expire_time = expire_time

    def get(self, key):
        """获取 redis 值"""
        cache_key = self.build_key(key)
        value = self.redis_client.get(cache_key)

        if value is None:
            return None

        try:
            ret = json.loads(value)
        except json.JSONDecodeError:
            ret = value
        return ret

    def delete(self, key):
        """删除指定 key"""
        cache_key = self.build_key(key)
        return self.redis_client.delete(cache_key)

    def set(self, key, value, expire=None, is_json=True):
        """设置键值对"""
        cache_key = self.build_key(key)
        if expire is None:
            expire = self.expire_time
        set_value = json.dumps(value) if is_json else value
        return self.redis_client.set(cache_key, set_value, ex=expire)

    def get_or_set(self, key, set_value, expire=None, is_json=True):
        """
        获取值, 如果不存在则存入 set_value
        """
        value = self.get(key)
        if value is not None:
            return value
        self.set(key, set_value, expire=expire, is_json=is_json)
        return set_value

    def key_exists(self, key):
        cache_key = self.build_key(key)
        return self.redis_client.exists(cache_key)

    def hget(self, key, field):
        cache_key = self.build_key(key)
        return self.redis_client.hget(cache_key, field)
    
    def hset(self, key, field, value, expire=None, is_json=True):
        cache_key = self.build_key(key)
        expire = self.expire_time if expire is None else expire
        set_value = json.dumps(value) if is_json else value
        return self.redis_client.hset(cache_key, field, set_value, expire)

    def build_key(self, key):
        assert isinstance(key, str), '设置 redis 的 key 非字符串'
        return '{}{}'.format(self.key_prefix, key)
    



class RedisQueue():
        __key_prefix = "kithubs:queue:{}:" 

        queue_name = None

        def __init__(self, queue_name:str, expire_time=-1):
            self.queue_name =self.__key_prefix + queue_name
            self.config = redis_config
            self.redis_client = redis.Redis(
                host=self.config.HOST, port=self.config.PORT, db=self.config.DB, password=self.config.PASSWORD,
                encoding="utf-8", decode_responses=True)
            
            self.expire_time = expire_time

        def enqueue(self, item):
            """Add an item to the queue (FIFO)."""
            return self.redis_client.lpush(self.queue_name, json.dumps(item))

        def dequeue(self, timeout=0):
            """Remove and return an item from the queue. Blocks if timeout > 0."""
            item = self.redis_client.brpop(self.queue_name, timeout=timeout)
            if item:
                # item is a tuple (queue_name, data)
                return json.loads(item[1])
            return None
        
        def size(self):
            """Return the number of items in the queue."""
            return self.redis.llen(self.queue_name)

        def clear(self):
            """Clear the queue."""
            return self.redis.delete(self.queue_name)