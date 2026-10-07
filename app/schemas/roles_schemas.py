from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RolesReq(BaseModel):
    name: str
    description: str


class RolesData(BaseModel):
    name: str
    description: str
    id: str
    created_at: datetime

class AllRolesRes(BaseModel):
    status: int
    message: str
    data: list[RolesData]

    model_config = ConfigDict(from_attributes=True)


class RolesRes(BaseModel):
    status: int
    message: str
    data: RolesData

    model_config = ConfigDict(from_attributes=True)
