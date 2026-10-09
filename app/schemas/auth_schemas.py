from pydantic import BaseModel, ConfigDict, EmailStr

from datetime import datetime


class RegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: int
    role_id: str


class RegisterData(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: int
    role_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AllUserResponse(BaseModel):
    status: int
    data: list[RegisterData]
    message: str

    model_config = ConfigDict(from_attributes=True)


class RegisterRes(BaseModel):
    status: int
    data: RegisterData
    message: str

    model_config = ConfigDict(from_attributes=True)


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class LoginData(BaseModel):
    id: str
    role_id: str
    phone: int
    is_active: bool
    token: str


class LoginRes(BaseModel):
    status: int
    data: LoginData
    message: str

    model_config = ConfigDict(from_attributes=True)
