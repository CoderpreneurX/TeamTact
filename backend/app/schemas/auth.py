from pydantic import BaseModel, EmailStr
from typing import Optional


class RequestPasswordReset(BaseModel):
    email: EmailStr


class PerformPasswordReset(BaseModel):
    token: Optional[str] = None
    new_password: str


class ResetResponse(BaseModel):
    message: str

class ValidateResetPasswordToken(BaseModel):
    code: Optional[str] = None

class VerifyEmail(BaseModel):
    token: str

class ResendVerificationEmail(BaseModel):
    email: EmailStr
