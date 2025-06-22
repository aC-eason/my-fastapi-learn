from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool  # 引入 QueuePool 作为连接池
from config.config import DEBUG, MysqlConfig

mysql_config =  MysqlConfig() 

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}/{}".format(
    mysql_config.username, mysql_config.password, mysql_config.inner, mysql_config.db
)


# 配置连接池
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,   # 使用 QueuePool 连接池（默认池类型）
    pool_size=10,          # 设置连接池大小为 10
    max_overflow=50,       # 超过池大小的最大连接数为 20
    pool_timeout=30,       # 获取连接的最大超时时间为 30 秒
    pool_recycle=3600,     # 每个连接生命周期最大为 1 小时
    pool_pre_ping=True    # 启用自动重连机制
)

# 创建 SessionLocal 类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 基类
Base = declarative_base()
