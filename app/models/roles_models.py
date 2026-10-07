from app.db.database import BASE
from sqlalchemy import Column, String, TIMESTAMP, text
import uuid


class RolesModel(BASE):
    __tablename__ = "roles"

    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )

    name = Column(String, nullable=False)

    description = Column(String, nullable=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
