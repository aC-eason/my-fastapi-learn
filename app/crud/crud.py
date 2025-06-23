import json
from datetime import datetime
from model.mysql.user import User
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError

# from utils.log_utils import ap_user_action, format_log_detail
from wrapper.db_wrapper import with_db_session
from model.mysql.short_url_mapping import ShortUrlMap


class UserDAO:
    def get_user(self, db: Session, **filters) -> Optional[User]:
        """通用查询用户方法，可通过 email 或 id 查询"""
        try:
            return db.query(User).filter_by(**filters).first()
        except SQLAlchemyError as e:
            # log_detail = format_log_detail(
            #     detail="get user error: {}".format(e), type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
            return None  # 避免程序崩溃，返回 None

    def create_user(
        self,
        db: Session,
        new_user: User,
    ):
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="create new user error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
            return None  # 避免程序崩溃

    def update_user_login_info(
        self,
        db: Session,
        email: str,
        last_login_ip: str,
        avatar: str = "",
        password: str = None,
        google_avatar: str = "",
    ):
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.last_login_ip = last_login_ip
                user.last_login_time = datetime.now()
                # 用户头像修改，更新图片链接
                if google_avatar and user.raw_avatar != google_avatar:
                    user.raw_avatar = google_avatar
                if avatar:
                    user.avatar = avatar
                if password:
                    user.password = password
                db.commit()
                db.refresh(user)
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="update  login info error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
            return None  # 避免程序崩溃

    @with_db_session
    def active_user(self, db: Session, user_id: int):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.status = 1
                db.commit()
                db.refresh(user)
                return user
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="active user error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
        return None

    def change_user_status(self, db: Session, user_id: int, status: int):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.status = status
                db.commit()
                db.refresh(user)
                return True
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="change user status error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
        return False

    def update_user_password(self, db: Session, user_id: int, password: str):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.password = password
                db.commit()
                db.refresh(user)
                return True
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="update user password error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
        return False

    def update_user_name(self, db: Session, user_id: int, user_name: str):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user.user_name = user_name
                db.commit()
                db.refresh(user)
                return True
        except SQLAlchemyError as e:
            db.rollback()  # 发生异常，回滚事务
            # log_detail = format_log_detail(
            #     detail="update user name error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
        return False


user_dao = UserDAO()


class ShortUrlMappingDAO:

    def create_short_url_mapping(self, mapping):
        try:
            self.db.add(mapping)
            self.db.commit()
            self.db.refresh(mapping)
            return mapping
        except SQLAlchemyError as e:
            self.db.rollback()
            # log_detail = format_log_detail(
            #     detail="create short url mapping error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
            return None

    @with_db_session
    def get_short_url_mapping(self, db: Session = None, **kwargs):
        try:
            return db.query(ShortUrlMap).filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            # log_detail = format_log_detail(
            #     detail="get short url mapping error", type="Datebase Error"
            # )
            # ap_user_action.error(log_detail)
            return None

short_url_mapping_dao = ShortUrlMappingDAO()
