from pydantic import BaseModel, validator


class LoginFromBase(BaseModel):
    invite_code :str = None

class GoogleLogin(LoginFromBase):
    client_id: str


class EmailForm(LoginFromBase):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        if not "@" in v:
            raise ValueError("Invalid email format")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8 or len(v) > 20:
            raise ValueError("Password must be  8 ~ 20 characters")
        return v
