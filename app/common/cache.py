from core.redis_cache import RedisCache


VISIT_INFO =  RedisCache("visit_info", "", 86400)