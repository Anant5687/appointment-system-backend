from app.db.database import BASE
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Time, text

import uuid


class AvailabilityModel(BASE):
    __tablename__ = "availability"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)

    location_id = Column(String, ForeignKey("locations.id"), nullable=False)

    day_of_week = Column(Integer, nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    is_active = Column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
