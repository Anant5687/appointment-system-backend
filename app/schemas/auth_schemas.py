from pydantic import BaseModel, ConfigDict, EmailStr

from datetime import datetime


class RegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: int
    role: str

    model_config = ConfigDict(from_attributes=True)


class RegisterRes(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class LoginData(BaseModel):
    id: str
    role: str
    phone: int
    is_active: bool
    token: str


class LoginRes(BaseModel):
    status: int
    data: LoginData
    message: str

    model_config = ConfigDict(from_attributes=True)
