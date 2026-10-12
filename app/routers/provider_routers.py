from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.users_models import UsersModel
from app.schemas.provider_schemas import (
    AvailabilityCreateReq,
    AvailabilityListRes,
    AvailabilityRes,
    AvailabilityUpdateReq,
    ProviderListRes,
    ProviderRes,
)
from app.services.provider_service import ProviderService

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("", response_model=ProviderListRes)
def get_providers(db: Session = Depends(get_db)):
    try:
        return ProviderService.get_providers(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/me/availability", response_model=AvailabilityListRes)
def get_my_availability(
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return ProviderService.get_my_availability(current_user.id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.post(
    "/me/availability", response_model=AvailabilityRes, status_code=201
)
def create_my_availability(
    data: AvailabilityCreateReq,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return ProviderService.create_my_availability(current_user.id, data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.patch("/me/availability/{availability_id}", response_model=AvailabilityRes)
def update_my_availability(
    availability_id: str,
    data: AvailabilityUpdateReq,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return ProviderService.update_my_availability(
            current_user.id, availability_id, data, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.delete("/me/availability/{availability_id}", response_model=AvailabilityRes)
def delete_my_availability(
    availability_id: str,
    db: Session = Depends(get_db),
    current_user: UsersModel = Depends(get_current_user),
):
    try:
        return ProviderService.delete_my_availability(
            current_user.id, availability_id, db
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/{provider_id}/availability", response_model=AvailabilityListRes)
def get_provider_availability(
    provider_id: str, db: Session = Depends(get_db)
):
    try:
        return ProviderService.get_provider_availability(provider_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/{provider_id}", response_model=ProviderRes)
def get_provider_by_id(provider_id: str, db: Session = Depends(get_db)):
    try:
        return ProviderService.get_provider_by_id(provider_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
