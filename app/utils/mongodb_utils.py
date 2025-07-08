from config.config import MongoDBConfig
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson import ObjectId
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from utils.log_utils import logger_access


class MongoDBClient:
    """MongoDB 连接管理工具类，包含连接池、资源控制和用户权限管理"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """实现单例模式，确保全局只有一个 MongoDB 客户端实例"""
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        host: str = "10.4.4.10",
        port: int = 27017,
    ):
        """初始化 MongoDB 客户端"""
        if not hasattr(self, "_initialized"):  # 避免重复初始化
            try:
                # 使用环境变量覆盖默认配置（生产环境推荐）

                self.uri = os.getenv(
                    "MONGO_URI",
                    f"mongodb://{MongoDBConfig.username}:{MongoDBConfig.password}@{MongoDBConfig.inner}:{MongoDBConfig.port}/",
                )
                self.db_name = os.getenv("MONGO_DB_NAME", MongoDBConfig.db_name)

                # 配置连接池和超时
                self.client = MongoClient(
                    self.uri,
                    serverSelectionTimeoutMS=5000,  # 连接超时 5 秒
                    maxPoolSize=50,  # 最大连接池大小
                    minPoolSize=5,  # 最小连接池大小
                    maxIdleTimeMS=10000,  # 空闲连接最大存活时间 10 秒
                )

                # 测试连接
                self.client.admin.command("ping")
                self.db = self.client[self.db_name]
                logger_access.info(
                    f"Connected to MongoDB at {host}:{port}, database: {self.db_name}"
                )

                # 用户权限配置（示例：存储用户角色）
                self.user_roles = {
                    "admin": ["read", "write", "admin"],
                    "user": ["read"],
                    "guest": ["read_limited"],
                }

                self._initialized = True
            except ConnectionFailure as e:
                logger_access.error(f"Failed to connect to MongoDB: {e}")
                raise
            except Exception as e:
                logger_access.error(
                    f"Unexpected error during MongoDB initialization: {e}"
                )
                raise

    @contextmanager
    def get_collection(self, collection_name: str):
        """上下文管理器，获取集合并确保资源释放"""
        try:
            collection = self.db[collection_name]
            yield collection
        except Exception as e:
            logger_access.error(f"Error accessing collection {collection_name}: {e}")
            raise
        finally:
            pass  # MongoClient 自动管理连接，无需手动关闭

    def find_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        projection: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """查询单个文档"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.find_one(query, projection)
                if result and "_id" in result:
                    result["id"] = str(result["_id"])  # 转换 ObjectId 为字符串
                    del result["_id"]
                return result
            except Exception as e:
                logger_access.error(f"Error in find_one for {collection_name}: {e}")
                raise

    def find_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        projection: Optional[Dict] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> List[Dict]:
        """查询多个文档，支持分页"""
        with self.get_collection(collection_name) as collection:
            try:
                cursor = collection.find(query, projection).skip(skip).limit(limit)
                results = [
                    {**doc, "id": str(doc["_id"]), "_id": None} for doc in cursor
                ]
                return [doc for doc in results if doc["_id"] is None]
            except Exception as e:
                logger_access.error(f"Error in find_many for {collection_name}: {e}")
                raise

    def aggregate(
        self, collection_name: str, pipeline: List[Dict], username: str
    ) -> List[Dict]:
        """执行聚合查询"""
        with self.get_collection(collection_name) as collection:
            try:
                results = list(collection.aggregate(pipeline))
                # 转换 ObjectId 为字符串
                for doc in results:
                    if "_id" in doc and isinstance(doc["_id"], ObjectId):
                        doc["id"] = str(doc["_id"])
                        del doc["_id"]
                return results
            except Exception as e:
                logger_access.error(f"Error in aggregate for {collection_name}: {e}")
                raise

    def insert_one(
        self, collection_name: str, document: Dict[str, Any], username: str
    ) -> str:
        """插入单个文档，返回插入的 ID"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.insert_one(document)
                return str(result.inserted_id)
            except Exception as e:
                logger_access.error(f"Error in insert_one for {collection_name}: {e}")
                raise

    def insert_many(
        self, collection_name: str, documents: List[Dict[str, Any]], username: str
    ) -> List[str]:
        """批量插入多个文档，返回插入的 ID 列表"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.insert_many(documents)
                return [str(_id) for _id in result.inserted_ids]
            except Exception as e:
                logger_access.error(f"Error in insert_many for {collection_name}: {e}")
                raise

    def update_one(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False,
    ) -> Dict[str, Any]:
        """更新单个文档，返回更新结果"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.update_one(query, {"$set": update}, upsert=upsert)
                return {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                    "upserted_id": (
                        str(result.upserted_id) if result.upserted_id else None
                    ),
                }
            except Exception as e:
                logger_access.error(f"Error in update_one for {collection_name}: {e}")
                raise

    def update_many(
        self,
        collection_name: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False,
    ) -> Dict[str, Any]:
        """批量更新多个文档，返回更新结果"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.update_many(query, {"$set": update}, upsert=upsert)
                return {
                    "matched_count": result.matched_count,
                    "modified_count": result.modified_count,
                    "upserted_id": (
                        str(result.upserted_id) if result.upserted_id else None
                    ),
                }
            except Exception as e:
                logger_access.error(f"Error in update_many for {collection_name}: {e}")
                raise

    def delete_one(
        self, collection_name: str, query: Dict[str, Any], username: str
    ) -> int:
        """删除单个文档，返回删除的文档数"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.delete_one(query)
                return result.deleted_count
            except Exception as e:
                logger_access.error(f"Error in delete_one for {collection_name}: {e}")
                raise

    def delete_many(
        self, collection_name: str, query: Dict[str, Any], username: str
    ) -> int:
        """批量删除多个文档，返回删除的文档数"""

        with self.get_collection(collection_name) as collection:
            try:
                result = collection.delete_many(query)
                return result.deleted_count
            except Exception as e:
                logger_access.error(f"Error in delete_many for {collection_name}: {e}")
                raise

    def close(self):
        """关闭 MongoDB 连接"""
        if self.client:
            self.client.close()
            logger_access.info("MongoDB connection closed")
            self._initialized = False

    def __del__(self):
        """确保对象销毁时关闭连接"""
        self.close()
