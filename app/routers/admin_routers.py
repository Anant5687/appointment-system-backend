from app.services.admin_services import AdminService
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from app.schemas.auth_schemas import AllUserResponse, RegisterRes, RegisterReq
from app.schemas.booking_schemas import BookingRes, BookingReq, AllBookingRes

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AllUserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        AdminService.get_all_users(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/user/{user_id}", response_model=list[RegisterRes])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    try:
        AdminService.get_user_by_id(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/user/{user_id}", response_model=RegisterRes)
def update_user(user_id: str, data: RegisterReq, db: Session = Depends(get_db)):
    try:
        AdminService.update_user(user_id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.delete("/user/{user_id}", response_model=RegisterRes)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        AdminService.delete_user(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/bookings", response_model=AllBookingRes)
def all_bookings(db: Session = Depends(get_db)):
    try:
        AdminService.all_bookings(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/booking/{booking_id}", response_model=BookingRes)
def update_booking(booking_id: str, data: BookingReq, db: Session = Depends(get_db)):
    try:
        AdminService.update_booking(booking_id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
