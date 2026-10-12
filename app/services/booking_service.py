from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.booking_schemas import BookingCreateReq, BookingUpdateReq
from app.models.bookings_models import BookingsModel
from app.models.enums import BookingStatus
from app.models.providers_models import ProviderModel


class BookingService:
    @staticmethod
    def __provider_id_for_user__(user_id: str, db: Session):
        provider = (
            db.query(ProviderModel)
            .filter(ProviderModel.user_id == user_id)
            .first()
        )
        return provider.id if provider else None

    @staticmethod
    def __check_booking__(booking_id: str, user_id: str, db: Session):
        booking = (
            db.query(BookingsModel)
            .filter(BookingsModel.id == booking_id)
            .first()
        )
        if not booking:
            raise HTTPException(
                status_code=404, detail=f"Booking not found with {booking_id}"
            )

        if booking.customer_id != user_id:
            raise HTTPException(status_code=403, detail="Booking access denied")

        return booking

    @staticmethod
    def create_booking(data: BookingCreateReq, user_id: str, db: Session):
        new_booking = BookingsModel(
            customer_id=user_id,
            status=BookingStatus.PENDING,
            **data.model_dump(),
        )
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)

        return {
            "status": 201,
            "message": "Booking created successfully",
            "data": new_booking,
        }

    @staticmethod
    def get_bookings(user_id: str, db: Session):
        bookings = (
            db.query(BookingsModel)
            .filter(BookingsModel.customer_id == user_id)
            .all()
        )

        return {
            "status": 200,
            "message": "Bookings data fetched successfully",
            "data": bookings,
        }

    @staticmethod
    def get_booking_by_id(booking_id: str, user_id: str, db: Session):
        check_booking = BookingService.__check_booking__(booking_id, user_id, db)

        return {
            "status": 200,
            "message": "Booking data fetched successfully",
            "data": check_booking,
        }

    @staticmethod
    def cancel_booking(booking_id: str, user_id: str, db: Session):
        booking = BookingService.__check_booking__(booking_id, user_id, db)
        if booking.status not in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
            raise HTTPException(
                status_code=409, detail="Booking cannot be cancelled in its current status"
            )

        booking.status = BookingStatus.CANCELLED
        db.commit()
        db.refresh(booking)

        return {
            "status": 200,
            "message": "Booking cancelled successfully",
            "data": booking,
        }

    @staticmethod
    def update_meeting(
        booking_id: str, data: BookingUpdateReq, user_id: str, db: Session
    ):
        booking = BookingService.__check_booking__(booking_id, user_id, db)
        if booking.status not in (BookingStatus.PENDING, BookingStatus.CONFIRMED):
            raise HTTPException(
                status_code=409,
                detail="Booking cannot be rescheduled in its current status",
            )

        for key, value in data.model_dump().items():
            setattr(booking, key, value)

        db.commit()
        db.refresh(booking)

        return {
            "status": 200,
            "message": "Booking updated successfully",
            "data": booking,
        }

    @staticmethod
    def get_provider_bookings(user_id: str, db: Session):
        provider = (
            db.query(ProviderModel)
            .filter(
                ProviderModel.user_id == user_id,
                ProviderModel.is_active.is_(True),
            )
            .first()
        )
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider profile not found")
        return {
            "status": 200,
            "message": "Provider bookings fetched successfully",
            "data": db.query(BookingsModel)
            .filter(BookingsModel.provider_id == provider.id)
            .all(),
        }

    @staticmethod
    def update_provider_booking_status(
        booking_id: str,
        user_id: str,
        status: BookingStatus,
        db: Session,
    ):
        provider = (
            db.query(ProviderModel)
            .filter(
                ProviderModel.user_id == user_id,
                ProviderModel.is_active.is_(True),
            )
            .first()
        )
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider profile not found")

        booking = (
            db.query(BookingsModel)
            .filter(
                BookingsModel.id == booking_id,
                BookingsModel.provider_id == provider.id,
            )
            .first()
        )
        if booking is None:
            raise HTTPException(status_code=404, detail="Booking not found")

        allowed_current_status = {
            BookingStatus.CONFIRMED: (BookingStatus.PENDING,),
            BookingStatus.COMPLETED: (BookingStatus.CONFIRMED,),
            BookingStatus.NO_SHOW: (BookingStatus.CONFIRMED,),
        }
        if booking.status not in allowed_current_status[status]:
            raise HTTPException(
                status_code=409,
                detail=f"Booking cannot be marked {status.value} in its current status",
            )

        booking.status = status
        db.commit()
        db.refresh(booking)
        return {
            "status": 200,
            "message": f"Booking marked {status.value.lower()} successfully",
            "data": booking,
        }
