# import pytz
from utils.db_utils import Base


# beijing_tz = pytz.timezone("Asia/Shanghai")


class CommonModel(Base):
    """通用模型基类，提供字段整理功能"""

    __abstract__ = True  # 声明为抽象基类，不创建实际表

    # def trans_time(self, filed_value) :
    #     """
    #     数据库时区问题统一处理成北京时区,
    #     返回一个时间对象
    #     """
    #     return beijing_tz.localize(filed_value)
