from pydantic import BaseModel, ConfigDict
from datetime import date, time, datetime


class BookingReq(BaseModel):
    customer_id: str
    provider_id: str
    service_id: str
    location_id: str
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    notes: str


class BookingResData(BaseModel):
    id: str
    customer_id: str
    provider_id: str
    service_id: str
    location_id: str
    appointment_date: date
    start_time: time
    end_time: time
    status: str
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BookingRes(BaseModel):
    status: int
    message: str
    data: BookingResData

    model_config = ConfigDict(from_attributes=True)


class AllBookingRes(BaseModel):
    status: int
    message: str
    data: list[BookingResData]

    model_config = ConfigDict(from_attributes=True)

class BookingUpdateReq(BaseModel):
    appointment_date: date
    start_time: time
    end_time: time
    provider_id: str
    location_id: str
