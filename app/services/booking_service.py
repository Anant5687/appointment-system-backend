from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.booking_schemas import BookingReq, BookingUpdateReq
from app.models.bookings_models import BookingsModel


class BookingService:
    def __check_booking__(booking_id: str, db: Session):
        booking = db.query(BookingsModel.id == booking_id).first()
        if not booking:
            raise HTTPException(
                status_code=404, detail=f"Booking not found with {booking_id}"
            )

        return booking

    @staticmethod
    def create_booking(data: BookingReq, db: Session):
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
    def get_bookings(db: Session):
        bookings = db.query(BookingsModel).all()

        return {
            "status": 200,
            "message": "Bookings data fetched successfully",
            "data": bookings,
        }

    @staticmethod
    def get_booking_by_id(booking_id: str, db: Session):
        check_booking = BookingService.__check_booking__(booking_id, db)

        return {
            "status": 200,
            "message": "Booking data fetched successfully",
            "data": check_booking,
        }

    @staticmethod
    def cancel_booking(booking_id: str, db: Session):
        booking = BookingService.__check_booking__(booking_id, db)

        booking.status = "CANCELLED"
        db.commit()
        db.refresh(booking)

        return {
            "status": 200,
            "message": "Booking cancelled successfully",
            "data": booking,
        }

    @staticmethod
    def update_meeting(booking_id: str, data: BookingUpdateReq, db: Session):
        booking = BookingService.__check_booking__(booking_id, db)

        for key, value in data.dict().items():
            setattr(booking, key, value)

        db.commit()
        db.refresh(booking)

        return {
            "status": 200,
            "message": "Booking updated successfully",
            "data": booking,
        }
