from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from model.mysql.common_model import CommonModel





class User(CommonModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    email = Column(String(191), unique=True, nullable=False, comment="邮箱")
    password = Column(String(255), nullable=False, comment="哈希后的用户密码")
    user_name = Column(String(100), default="", comment="用户名")
    avatar = Column(String(150), default="", comment="头像")
    raw_avatar = Column(String(150), default="", comment="原始用户头像")
    register_time = Column(TIMESTAMP, server_default=func.now(), comment="用户注册时间")
    last_login_ip = Column(String(45), nullable=True, comment="用户上一次登录IP")
    last_login_time = Column(TIMESTAMP, server_default=func.now(), comment="用户最近登录时间")
    register_ip = Column(String(45), nullable=True, comment="用户登录IP")
    user_type = Column(Integer, default=1, comment="用户类型")
    status = Column(Integer, default=0, comment="用户状态")
    is_deleted = Column(Integer, default=0, comment="是否删除")
    created_at = Column(TIMESTAMP, server_default=func.now(), comment="数据创建时间")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), comment="数据更新时间")
    invite_code  = Column(String(50), default="", comment="用户注册邀请码")
    
    def get_created_at(self):
        # 统一转时区方法
        return self.trans_time(self.created_at)

