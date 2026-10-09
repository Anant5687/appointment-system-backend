from app.models.users_models import UsersModel
from app.models.bookings_models import BookingsModel
from sqlalchemy.orm import Session

from app.schemas.auth_schemas import RegisterReq
from app.schemas.booking_schemas import BookingReq

from fastapi import HTTPException


class AdminService:

    def __user_exist__(user_id: str, db: Session):
        is_user = db.query(UsersModel).filter(UsersModel.id == user_id).first()

        if not user_id:
            raise HTTPException(
                status_code=404, detail=f"User not found with {user_id}"
            )

        return is_user

    @staticmethod
    def get_all_users(db: Session):
        return {
            "data": db.query(UsersModel).filter(UsersModel.is_active).all(),
            "status": 200,
            "message": "User data successfully fetched",
        }

    @staticmethod
    def get_user_by_id(user_id: str, db: Session):
        user = AdminService.__user_exist__(user_id, db)
        return {
            "data": user,
            "status": 200,
            "message": "User data successfully fetched",
        }

    @staticmethod
    def update_user(user_id: str, data: RegisterReq, db: Session):
        user = AdminService.__user_exist__(user_id, db)

        for key, value in data.dict().items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return {"status": 200, "message": "User updated successfully", "data": user}

    @staticmethod
    def delete_user(user_id: str, db: Session):
        user = AdminService.__user_exist__(user_id, db)

        db.delete(user)
        db.commit()

        return {"status": 200, "message": "User deleted successfully", "data": user}

    @staticmethod
    def all_bookings(db: Session):
        return {
            "data": db.query(BookingsModel).all(),
            "status": 200,
            "message": "User data successfully fetched",
        }

    @staticmethod
    def update_booking(booking_id: str, data: BookingReq, db: Session):
        is_booking = (
            db.query(BookingsModel).filter(BookingsModel.id == booking_id).first()
        )

        if not is_booking:
            raise HTTPException(
                status_code=404, detail=f"Booking not found with {booking_id}"
            )

        for key, value in data.dict().items():
            setattr(is_booking, key, value)

        db.commit()
        db.refresh(is_booking)

        return {
            "status": 200,
            "message": "Booking updated successfully",
            "data": is_booking,
        }
