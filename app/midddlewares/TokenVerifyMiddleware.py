import re
from fastapi import HTTPException
from utils.log_utils import logger_access
from starlette.middleware.base import BaseHTTPMiddleware

# 定义可疑 User-Agent 的模式
SUSPICIOUS_PATTERNS = [
    r"bot",
    r"crawler",
    r"spider",
    r"python-requests",
    r"curl",
    r"scrapy",
    r"wget",
    r"httpclient",
    r"java/",
    r"phantomjs",
    r"^mozilla/5\.0$",  # 精确匹配 Mozilla/5.0
]

# 定义 User-Agent 最小长度
MIN_USER_AGENT_LENGTH = 20  # 正常浏览器的 User-Agent 通常较长

class TokenVerifyMiddleware(BaseHTTPMiddleware):
    # dispatch 必须实现
    async def dispatch(self, request, call_next):
        user_agent = request.headers.get("User-Agent", "").strip()
            # 检查是否缺少 User-Agent
        if not user_agent:
            logger_access.warning(f"Blocked request from {request.client.host}: No User-Agent provided")
            raise HTTPException(status_code=403, detail="No User-Agent provided")
        
        # 检查 User-Agent 长度
        if len(user_agent) < MIN_USER_AGENT_LENGTH:
            logger_access.warning(f"Blocked request from {request.client.host}: User-Agent too short: {user_agent}")
            raise HTTPException(status_code=403, detail="User-Agent too short")
        
        # 检查是否匹配可疑模式（包括 Mozilla/5.0）
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, user_agent.lower(), re.IGNORECASE):
                logger_access.warning(f"Blocked request from {request.client.host}: Suspicious User-Agent: {user_agent}")
                raise HTTPException(status_code=403, detail="Suspicious User-Agent detected")
        
        # 继续处理正常请求
        response = await call_next(request)
        return response
