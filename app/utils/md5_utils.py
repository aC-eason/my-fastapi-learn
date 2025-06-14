import hashlib
import uuid


def md5(str_):
    return hashlib.md5(str_.encode("utf-8")).hexdigest()


def generate_random_md5():
    random_str = str(uuid.uuid4())  # 使用 UUID 生成随机字符串
    return md5(random_str)
