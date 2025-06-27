from core.redis_cache import RedisCache

from core.redis_core import RedisQueue


VISIT_INFO =  RedisCache("visit_info", "", 86400)

TOKEN_CACHE = RedisCache("token_cache", "", 60 * 60 * 24 * 7)

SHORT_URL_CACHE = RedisCache("short_url_cache", "", 60 * 60 *24)

VISIT_SHORT_URL_CACHE = RedisQueue(queue_name="visit_short_queue")