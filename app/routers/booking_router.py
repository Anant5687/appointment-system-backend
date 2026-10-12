from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db

from app.services.booking_service import BookingService
from app.schemas.booking_schemas import (
    BookingCreateReq,
    BookingRes,
    AllBookingRes,
    BookingUpdateReq,
)
from app.core.auth import get_current_user
from app.models.users_models import UsersModel
from app.models.enums import BookingStatus

router = APIRouter(prefix="/bookings", tags=["Bookings"])
provider_router = APIRouter(prefix="/provider/bookings", tags=["Provider Bookings"])


@router.post("", response_model=BookingRes, status_code=201)
@router.post("/create", response_model=BookingRes, status_code=201, include_in_schema=False)
def create_booking(
    data: BookingCreateReq,
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


@router.get("", response_model=AllBookingRes)
@router.get("/all", response_model=AllBookingRes, include_in_schema=False)
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


@router.patch("/{booking_id}/reschedule", response_model=BookingRes)
@router.post(
    "/{booking_id}/reschedule",
    response_model=BookingRes,
    include_in_schema=False,
)
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


@provider_router.get("", response_model=AllBookingRes)
def get_provider_bookings(
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.get_provider_bookings(current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@provider_router.patch("/{booking_id}/confirm", response_model=BookingRes)
def confirm_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.update_provider_booking_status(
            booking_id, current_user.id, BookingStatus.CONFIRMED, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@provider_router.patch("/{booking_id}/complete", response_model=BookingRes)
def complete_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.update_provider_booking_status(
            booking_id, current_user.id, BookingStatus.COMPLETED, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@provider_router.patch("/{booking_id}/no-show", response_model=BookingRes)
def no_show_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return BookingService.update_provider_booking_status(
            booking_id, current_user.id, BookingStatus.NO_SHOW, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
