from fastapi import FastAPI

from api.common.common_api import router as CommonRouter
from midddlewares.TokenVerifyMiddleware  import TokenVerifyMiddleware

app = FastAPI()

app.include_router(CommonRouter, prefix="/api")

# app.add_middleware(TokenVerifyMiddleware)


