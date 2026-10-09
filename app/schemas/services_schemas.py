from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ServiceReq(BaseModel):
    name: str
    description: str
    duration_minutes: int
    price: int


class ServiceReqData(BaseModel):
    id: str
    name: str
    description: str
    duration_minutes: int
    price: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceRes(BaseModel):
    status: int
    message: str
    data: ServiceReqData
    model_config = ConfigDict(from_attributes=True)


class AllServiceRes(BaseModel):
    status: int
    message: str
    data: list[ServiceReqData]
    model_config = ConfigDict(from_attributes=True)
