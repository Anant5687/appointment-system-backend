from app.services.admin_services import AdminService
from app.db.database import get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException, APIRouter, Depends
from app.schemas.auth_schemas import AllUserResponse, RegisterRes, RegisterReq
from app.schemas.booking_schemas import (
    AdminBookingUpdateReq,
    BookingRes,
    AllBookingRes,
)
from app.schemas.provider_schemas import (
    ProviderCreateReq,
    ProviderRes,
    ProviderUpdateReq,
)
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=list[AllUserResponse])
def get_all_users(db: Session = Depends(get_db)):
    try:
        return AdminService.get_all_users(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/user/{user_id}", response_model=list[RegisterRes])
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        return AdminService.get_user_by_id(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/user/{user_id}", response_model=RegisterRes)
def update_user(
    user_id: str,
    data: RegisterReq,
    db: Session = Depends(get_db),
):
    try:
        return AdminService.update_user(user_id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.delete("/user/{user_id}", response_model=RegisterRes)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        return AdminService.delete_user(user_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/bookings", response_model=AllBookingRes)
def all_bookings(db: Session = Depends(get_db)):
    try:
        return AdminService.all_bookings(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/bookings/{booking_id}", response_model=BookingRes)
@router.patch(
    "/booking/{booking_id}", response_model=BookingRes, include_in_schema=False
)
def update_booking(
    booking_id: str,
    data: AdminBookingUpdateReq,
    db: Session = Depends(get_db),
):
    try:
        return AdminService.update_booking(booking_id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.post("/providers", response_model=ProviderRes, status_code=201)
def create_provider(data: ProviderCreateReq, db: Session = Depends(get_db)):
    try:
        return ProviderService.create_provider(data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/providers/{provider_id}", response_model=ProviderRes)
def update_provider(
    provider_id: str,
    data: ProviderUpdateReq,
    db: Session = Depends(get_db),
):
    try:
        return ProviderService.update_provider(provider_id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.delete("/providers/{provider_id}", response_model=ProviderRes)
def delete_provider(provider_id: str, db: Session = Depends(get_db)):
    try:
        return ProviderService.delete_provider(provider_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
