from app.db.database import BASE
from app.models.enums import IndianState
from sqlalchemy import Boolean, Column, Enum, String, TIMESTAMP, text

import uuid


class LocationsModel(BASE):
    __tablename__ = "locations"
    id = Column(
        String, primary_key=True, nullable=False, default=lambda: str(uuid.uuid4())
    )
    name = Column(String, nullable=False)

    address = Column(String, nullable=False)

    city = Column(String, nullable=False)

    state = Column(
        Enum(
            IndianState,
            name="indian_state",
            native_enum=False,
            values_callable=lambda states: [state.value for state in states],
        ),
        nullable=False,
    )

    country = Column(String, nullable=False, default="India", server_default="India")

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
