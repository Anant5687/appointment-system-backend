from pydantic import BaseModel, ConfigDict, model_validator
from app.models.enums import BookingStatus
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
    notes: str | None = None


class BookingCreateReq(BaseModel):
    provider_id: str
    service_id: str
    location_id: str
    appointment_date: date
    start_time: time
    end_time: time
    notes: str | None = None

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


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
    notes: str | None
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

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class AdminBookingUpdateReq(BaseModel):
    customer_id: str | None = None
    provider_id: str | None = None
    service_id: str | None = None
    location_id: str | None = None
    appointment_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    status: BookingStatus | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Update fields cannot be null")
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValueError("end_time must be later than start_time")
        return self
