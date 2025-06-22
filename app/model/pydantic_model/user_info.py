from pydantic import BaseModel
from typing import Union

class UserInfo(BaseModel):
    user_id: Union[str, int] = 0
    is_login:bool = False