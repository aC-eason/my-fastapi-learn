import re
from pydantic import BaseModel

class SensitiveWordCheck(BaseModel):
    content:str