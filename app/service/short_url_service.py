import time
from copy import deepcopy
from fastapi import  Request
from sqlalchemy.orm import Session
from model.mysql.short_url_mapping import ShortUrlMap
from crud.crud import short_url_mapping_dao
from utils.common_utils import generate_short_code
from wrapper.db_wrapper import with_db_session
from common.cache import SHORT_URL_CACHE, VISIT_SHORT_URL_CACHE


class ShortUrlService:
    SHORT_CACHE_TEMPLATE = {
        "original_url": "",
        "short_code": "",
        "is_tracked": False,
        "user_id": 0,
    }

    def get_short_code(self,db: Session = None):
        """
        生成短链接code
        :param db: 数据库会话
        :return: 短链接code
        """
        while True:
            short_code = generate_short_code()
            # 检查短链接是否已存在
            existing_short_url = short_url_mapping_dao.get_short_url_mapping(
                short_code=short_code,is_deleted=0, db=db
            )
            if not existing_short_url:
                return short_code

    @with_db_session
    def create_short_url(
        self, origin_url, user_id, is_tracked=False, db: Session = None
    ):
        """
        创建短链接
        :param origin_url: 原始链接
        :param user_id: 用户ID
        :param is_tracked: 是否追踪，默认为False
        :return: 短链接的code
        """
        short_code = self.get_short_code(db)
        short_url_info = ShortUrlMap(
            user_id=user_id,
            short_code=short_code,
            original_url=origin_url,
            is_tracked=1 if is_tracked else 0,
        )
        shots = short_url_mapping_dao.create_short_url_mapping(
            db=db, mapping=short_url_info
        )
        if shots:
            # 缓存短链接信息
            cache_info = deepcopy(self.SHORT_CACHE_TEMPLATE)
            cache_info["original_url"] = origin_url
            cache_info["short_code"] = short_code
            cache_info["is_tracked"] = is_tracked
            cache_info["user_id"] = user_id
            cache_info["id"] = shots.id
            SHORT_URL_CACHE.set(short_code, cache_info)
            return short_code
        return None
    
    def get_short_url_list(self, user_id, db: Session = None):
        """
        获取用户的短链接列表
        :param user_id: 用户ID
        :param db: 数据库会话
        :return: 短链接列表
        """
        short_urls = short_url_mapping_dao.get_short_url_mapping(user_id=user_id,is_deleted=0, db=db)
        if not short_urls:
            return []

        short_list = []
        for short in short_urls:
            cache_info = deepcopy(self.SHORT_CACHE_TEMPLATE)
            cache_info["original_url"] = short.original_url
            cache_info["short_code"] = short.short_code
            cache_info["is_tracked"] = short.is_tracked
            cache_info["user_id"] = short.user_id
            cache_info["id"] = short.id
            SHORT_URL_CACHE.set(short.short_code, cache_info)
            short_list.append(cache_info)

        return short_list

    def get_url_info(self, short_code, request:Request):
        """
        获取短链接信息
        :param short_code: 短链接code
        :param db: 数据库会话
        :return: 短链接信息
        """
        cache_info = SHORT_URL_CACHE.get(short_code)
        if not cache_info:
            short_info = short_url_mapping_dao.get_short_url_mapping(short_code=short_code,is_deleted=0)
            if not short_info:
                return None
            # 如果缓存中没有短链接信息，则从数据库获取并缓存
            short_info = short_info[0]
            cache_info = deepcopy(self.SHORT_CACHE_TEMPLATE)
            cache_info["original_url"] = short_info.original_url
            cache_info["short_code"] = short_info.short_code
            cache_info["is_tracked"] = short_info.is_tracked
            cache_info["user_id"] = short_info.user_id
            cache_info["id"] = short_info.id
            SHORT_URL_CACHE.set(short_code, cache_info)

        origin_url= cache_info.get("original_url")
        is_tracked = cache_info.get("is_tracked", False)
        if is_tracked:
            # 如果需要追踪，则将短链接信息放入队列
            visit_info = {
                "id": cache_info.get("id"),
                "short_code": short_code,
                "user_id": cache_info.get("user_id"),
                "ip":request.state.log_info.get("ip", ""),
                "referer":request.state.log_info.get("referer", ""),
                "time":int(time.time())
            }
            VISIT_SHORT_URL_CACHE.enqueue(visit_info)

        return origin_url


        
short_url_service = ShortUrlService()