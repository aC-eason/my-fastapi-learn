from fastapi import FastAPI

from api.common.common_api import router as CommonRouter
from api.text_api.text_api import router as TextRouter
from midddlewares.TokenVerifyMiddleware  import TokenVerifyMiddleware

app = FastAPI()

app.include_router(CommonRouter, prefix="/api")
app.include_router(TextRouter, prefix="/api")

# app.add_middleware(TokenVerifyMiddleware)


