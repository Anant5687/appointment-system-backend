from app.db.database import BASE
from sqlalchemy import Column, String, text, TIMESTAMP, Integer, Boolean

import uuid


class ServicesModel(BASE):
    __tablename__ = "services"

    id = Column(
        String, default=lambda: str(uuid.uuid4()), primary_key=True, nullable=False
    )

    name = Column(String, nullable=False)

    description = Column(String, nullable=False)

    duration_minutes = Column(Integer, nullable=False)

    price = Column(Integer, nullable=False)

    is_active = Column(
        Boolean, nullable=True, default=True, server_default=text("true")
    )

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
