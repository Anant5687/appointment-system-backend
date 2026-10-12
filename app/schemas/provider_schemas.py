from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProviderCreateReq(BaseModel):
    user_id: str
    bio: str
    phone: str


class ProviderUpdateReq(BaseModel):
    bio: str | None = None
    phone: str | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def reject_null_updates(self):
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Update fields cannot be null")
        return self


class ProviderData(BaseModel):
    id: str
    user_id: str
    bio: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProviderRes(BaseModel):
    status: int
    message: str
    data: ProviderData


class ProviderListRes(BaseModel):
    status: int
    message: str
    data: list[ProviderData]


class AvailabilityCreateReq(BaseModel):
    location_id: str
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    is_active: bool = True

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be later than start_time")
        return self


class AvailabilityUpdateReq(BaseModel):
    location_id: str | None = None
    day_of_week: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    end_time: time | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if any(getattr(self, field) is None for field in self.model_fields_set):
            raise ValueError("Update fields cannot be null")
        if (
            self.start_time is not None
            and self.end_time is not None
            and self.end_time <= self.start_time
        ):
            raise ValueError("end_time must be later than start_time")
        return self


class AvailabilityData(BaseModel):
    id: str
    provider_id: str
    location_id: str
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class AvailabilityRes(BaseModel):
    status: int
    message: str
    data: AvailabilityData


class AvailabilityListRes(BaseModel):
    status: int
    message: str
    data: list[AvailabilityData]
