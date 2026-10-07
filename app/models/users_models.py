from app.db.database import BASE

from sqlalchemy import Column, String, text, Boolean, TIMESTAMP, Integer, ForeignKey

import uuid


class UsersModel(BASE):
    __tablename__ = "users"

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False
    )

    name = Column(String, nullable=False, unique=True)

    email = Column(String, nullable=False)

    password = Column(String, nullable=False)

    phone = Column(String, nullable=False, unique=True)

    role_id = Column(String, ForeignKey("roles.id"), nullable=False)

    is_active = Column(Boolean, nullable=True, default=True)

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
