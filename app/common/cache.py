from core.redis_cache import RedisCache


VISIT_INFO =  RedisCache("visit_info", "", 86400)

TOKEN_CACHE = RedisCache("token_cache", "", 60 * 60 * 24 * 7)