from app.db.database import BASE
from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP, text

import uuid


class ProviderModel(BASE):
    __tablename__ = "providers"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    bio = Column(String, nullable=False)

    phone = Column(String, nullable=False)

    is_active = Column(
        Boolean, nullable=False, default=True, server_default=text("true")
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
