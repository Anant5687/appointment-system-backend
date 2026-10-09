from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.services.booking_service import BookingService
from app.schemas.booking_schemas import (
    BookingReq,
    BookingRes,
    AllBookingRes,
    BookingUpdateReq,
)
from app.core.auth import get_current_user
from app.models.users_models import UsersModel

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/create", response_model=BookingRes)
def create_booking(
    data: BookingReq,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.create_booking(data, current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/all", response_model=AllBookingRes)
def get_bookings(
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.get_bookings(current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/{booking_id}", response_model=BookingRes)
def get_booking_by_id(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.get_booking_by_id(booking_id, current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/{booking_id}/cancel", response_model=BookingRes)
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.cancel_booking(booking_id, current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.post("/{booking_id}/reschedule", response_model=BookingRes)
def update_meeting(
    booking_id: str,
    data: BookingUpdateReq,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.update_meeting(
            booking_id, data, current_user.id, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
