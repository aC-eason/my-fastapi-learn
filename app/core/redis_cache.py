import json
import time
from contextlib import contextmanager

from core.redis_core import Redis
from utils.md5_utils import md5


class RedisCache(Redis):
    # 配置key的模板，线条:项目:版本:作用（比如 generate_result、credit）:域（比如 用户ID）
    __key_prefix = "kithubs:visit_info:{}:" 
    # 默认过期时间（默认1小时）
    __expire_time = 3600

    def __init__(self, first_prefix, second_prefix='', expire_time=3600):
        if second_prefix:
            key_prefix = self.__key_prefix.format(first_prefix) + '{}:'.format(second_prefix)
        else:
            key_prefix = self.__key_prefix.format(first_prefix)
        if not expire_time:
            expire_time = self.__expire_time
        super().__init__(key_prefix=key_prefix, expire_time=expire_time)

    def build_key(self, key):
        """ 构建redis key, 由于原有缓存可能会存在传入list的情况，这种情况取第一项来区分不同域的键值 """
        cache_key = key
        if isinstance(key, str):
            cache_key = cache_key if len(cache_key) <= 32 else md5(key)
        else:
            cache_key = md5(json.dumps(key))
        return super().build_key(cache_key)


@contextmanager
def delay_double_del_cache(key, first_prefix, second_prefix='', delay_time=0.1):
    """延时双删上下文管理器"""
    cache = RedisCache(first_prefix, second_prefix)
    cache.delete(key)
    yield
    if delay_time:
        time.sleep(delay_time)
    cache.delete(key)
