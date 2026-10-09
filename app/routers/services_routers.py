from fastapi import HTTPException, Depends, APIRouter
from app.services.services_services import ServicesService
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.services_schemas import ServiceRes, AllServiceRes

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/all", response_model=AllServiceRes)
def get_all_services(db: Session = Depends(get_db)):
    try:
        return ServicesService.get_services(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.get("/{service_id}", response_model=ServiceRes)
def get_services_by_id(service_id: str, db: Session):
    try:
        return ServicesService.get_service_by_id(service_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
