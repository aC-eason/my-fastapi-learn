from functools import wraps
from sqlalchemy.orm import Session
from utils.db_utils import SessionLocal
from utils.mongodb_utils import MongoDBClient


def with_db_session(func):
    """
    装饰器，用于自动管理数据库会话。(同一接口会多次数据库操作会创建多次数据库链接)
    1. 如果没有传递有效的 db 对象，则创建新的会话。
    2. 自动关闭新创建的会话（如果没有 db）。

    推荐使用接口级别数据库链接(db: Session = Depends(get_db)使用唯一数据库连接)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        db: Session = kwargs.get("db", None)
        create_session = False
        if db is None:
            create_session = True
            db = SessionLocal()
            kwargs["db"] = db
        try:
            return func(*args, **kwargs)
        finally:
            if create_session:
                db.close()

    return wrapper


def with_mongo_db_client(func):
    @wraps
    def wrapper(*args, **kwargs):
        mongo_client = MongoDBClient()
        try:
            kwargs["mongo_client"] = mongo_client
            return func(*args, **kwargs)
        finally:
            mongo_client.close()
    
    return wrapper
