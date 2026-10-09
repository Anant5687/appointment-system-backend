from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.services_models import ServicesModel


class ServicesService:
    @staticmethod
    def get_services(db: Session):
        return {
            "status": 200,
            "message": "Services fetched successfully",
            "data": db.query(ServicesModel).all(),
        }

    @staticmethod
    def get_service_by_id(service_id: str, db: Session):
        service_exist = (
            db.query(ServicesModel).filter(ServicesModel.id == service_id).first()
        )

        if not service_exist:
            raise HTTPException(
                status_code=404, detail=f"Service not found with {service_id}"
            )

        return {
            "status": 200,
            "message": "Service fetched successfully",
            "data": service_exist,
        }
