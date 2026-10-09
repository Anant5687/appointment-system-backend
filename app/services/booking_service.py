from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.booking_schemas import BookingReq, BookingUpdateReq
from app.models.bookings_models import BookingsModel
from app.models.providers_models import ProviderModel
from sqlalchemy import or_


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

        provider_id = BookingService.__provider_id_for_user__(user_id, db)
        if booking.customer_id != user_id and booking.provider_id != provider_id:
            raise HTTPException(status_code=403, detail="Booking access denied")

        return booking

    @staticmethod
    def create_booking(data: BookingReq, user_id: str, db: Session):
        provider_id = BookingService.__provider_id_for_user__(user_id, db)
        if data.customer_id != user_id and data.provider_id != provider_id:
            raise HTTPException(status_code=403, detail="Booking access denied")

        new_booking = BookingsModel(**data.model_dump())
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
        provider_id = BookingService.__provider_id_for_user__(user_id, db)
        access_filter = BookingsModel.customer_id == user_id
        if provider_id is not None:
            access_filter = or_(
                access_filter, BookingsModel.provider_id == provider_id
            )
        bookings = db.query(BookingsModel).filter(access_filter).all()

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

        booking.status = "CANCELLED"
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
        provider_id = BookingService.__provider_id_for_user__(user_id, db)
        if (
            booking.customer_id != user_id
            and data.provider_id != provider_id
        ):
            raise HTTPException(
                status_code=403,
                detail="Providers can only reschedule their own bookings",
            )

        for key, value in data.dict().items():
            setattr(booking, key, value)

        db.commit()
        db.refresh(booking)

        return {
            "status": 200,
            "message": "Booking updated successfully",
            "data": booking,
        }
