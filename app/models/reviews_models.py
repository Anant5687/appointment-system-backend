from app.db.database import BASE
from sqlalchemy import (
    CheckConstraint,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    text,
)

import uuid


class ReviewsModel(BASE):
    __tablename__ = "reviews"

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)

    customer_id = Column(String, ForeignKey("users.id"), nullable=False)

    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)

    rating = Column(Integer, nullable=False)

    comment = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
