from app.db.database import BASE
from app.models.enums import BookingStatus
from sqlalchemy import Column, Date, Enum, ForeignKey, String, Time, TIMESTAMP, text

import uuid


class BookingsModel(BASE):
    __tablename__ = "bookings"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    customer_id = Column(String, ForeignKey("users.id"), nullable=False)

    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)

    service_id = Column(String, ForeignKey("services.id"), nullable=False)

    location_id = Column(String, ForeignKey("locations.id"), nullable=False)

    appointment_date = Column(Date, nullable=False)

    start_time = Column(Time, nullable=False)

    end_time = Column(Time, nullable=False)

    status = Column(
        Enum(
            BookingStatus,
            name="booking_status",
            native_enum=False,
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        nullable=False,
        default=BookingStatus.PENDING,
        server_default=BookingStatus.PENDING.value,
    )

    notes = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
    )
