import time
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Request, status, Path
from body.text_body import SensitiveWordCheck
from service.text_service import text_service

router = APIRouter(tags=["通用api"],prefix="/text", responses={404: {"description": "Not found"}})

@router.post("/sensitiveWord/check")
def senesitive_word_check(request:Request,word_bdy:SensitiveWordCheck):
    has_sensitive_word, sensitive_word = text_service.check_word(word_bdy.content)
    resp = {
        "status":200,
        "has_sensitive_word":has_sensitive_word,
        "sensitive_word":sensitive_word
    }
    return JSONResponse(resp)
