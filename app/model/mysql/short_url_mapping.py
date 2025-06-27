from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from model.mysql.common_model import CommonModel


class ShortUrlMap(CommonModel):
    __tablename__ = 'short_url_map'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, comment='用户ID')
    short_code = Column(String(10), nullable=False, unique=True, comment='短链code')
    original_url = Column(String(2048), nullable=False, comment='原始链接')
    is_tracked = Column(Integer, default=0, comment='是否追踪，0:不追踪，1:追踪')
    is_deleted = Column(Integer, default=0, comment='标记删除字段')
    created_at = Column(DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
