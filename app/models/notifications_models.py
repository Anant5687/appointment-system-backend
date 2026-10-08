from app.db.database import BASE
from sqlalchemy import Boolean, Column, ForeignKey, String, TIMESTAMP, text

import uuid


class NotificationModels(BASE):
    __tablename__ = "notifications"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    type = Column(String, nullable=False)

    title = Column(String, nullable=False)

    message = Column(String, nullable=False)

    is_read = Column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
