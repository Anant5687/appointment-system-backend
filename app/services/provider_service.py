from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.availability_models import AvailabilityModel
from app.models.locations_models import LocationsModel
from app.models.providers_models import ProviderModel
from app.models.users_models import UsersModel
from app.schemas.provider_schemas import (
    AvailabilityData,
    AvailabilityCreateReq,
    AvailabilityUpdateReq,
    ProviderCreateReq,
    ProviderUpdateReq,
)


class ProviderService:
    @staticmethod
    def _get_provider(
        provider_id: str, db: Session, active_only: bool = True
    ) -> ProviderModel:
        query = db.query(ProviderModel).filter(ProviderModel.id == provider_id)
        if active_only:
            query = query.filter(ProviderModel.is_active.is_(True))
        provider = query.first()
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider not found")
        return provider

    @staticmethod
    def _get_provider_for_user(user_id: str, db: Session) -> ProviderModel:
        provider = (
            db.query(ProviderModel).filter(ProviderModel.user_id == user_id).first()
        )
        if provider is None:
            raise HTTPException(status_code=404, detail="Provider profile not found")
        return provider

    @staticmethod
    def get_providers(db: Session):
        return {
            "status": 200,
            "message": "Providers fetched successfully",
            "data": db.query(ProviderModel)
            .filter(ProviderModel.is_active.is_(True))
            .all(),
        }

    @staticmethod
    def get_provider_by_id(provider_id: str, db: Session):
        return {
            "status": 200,
            "message": "Provider fetched successfully",
            "data": ProviderService._get_provider(provider_id, db),
        }

    @staticmethod
    def create_provider(data: ProviderCreateReq, db: Session):
        user = db.query(UsersModel).filter(UsersModel.id == data.user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        existing_provider = (
            db.query(ProviderModel)
            .filter(ProviderModel.user_id == data.user_id)
            .first()
        )
        if existing_provider is not None:
            raise HTTPException(
                status_code=409, detail="User already has a provider profile"
            )

        provider = ProviderModel(**data.model_dump())
        db.add(provider)
        db.commit()
        db.refresh(provider)
        return {
            "status": 201,
            "message": "Provider created successfully",
            "data": provider,
        }

    @staticmethod
    def update_provider(provider_id: str, data: ProviderUpdateReq, db: Session):
        provider = ProviderService._get_provider(provider_id, db, active_only=False)
        for field, value in data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(provider, field, value)
        db.commit()
        db.refresh(provider)
        return {
            "status": 200,
            "message": "Provider updated successfully",
            "data": provider,
        }

    @staticmethod
    def delete_provider(provider_id: str, db: Session):
        provider = ProviderService._get_provider(provider_id, db, active_only=False)
        provider.is_active = False
        db.commit()
        db.refresh(provider)
        return {
            "status": 200,
            "message": "Provider deactivated successfully",
            "data": provider,
        }

    @staticmethod
    def get_provider_availability(provider_id: str, db: Session):
        ProviderService._get_provider(provider_id, db)
        availability = (
            db.query(AvailabilityModel)
            .filter(
                AvailabilityModel.provider_id == provider_id,
                AvailabilityModel.is_active.is_(True),
            )
            .all()
        )
        return {
            "status": 200,
            "message": "Provider availability fetched successfully",
            "data": availability,
        }

    @staticmethod
    def get_my_availability(user_id: str, db: Session):
        provider = ProviderService._get_provider_for_user(user_id, db)
        availability = (
            db.query(AvailabilityModel)
            .filter(AvailabilityModel.provider_id == provider.id)
            .all()
        )
        return {
            "status": 200,
            "message": "Provider availability fetched successfully",
            "data": availability,
        }

    @staticmethod
    def create_my_availability(user_id: str, data: AvailabilityCreateReq, db: Session):
        provider = ProviderService._get_provider_for_user(user_id, db)
        location = (
            db.query(LocationsModel)
            .filter(
                LocationsModel.id == data.location_id,
                LocationsModel.is_active.is_(True),
            )
            .first()
        )
        if location is None:
            raise HTTPException(status_code=404, detail="Active location not found")

        availability = AvailabilityModel(provider_id=provider.id, **data.model_dump())
        db.add(availability)
        db.commit()
        db.refresh(availability)
        return {
            "status": 201,
            "message": "Provider availability created successfully",
            "data": availability,
        }

    @staticmethod
    def _get_my_availability_record(
        user_id: str, availability_id: str, db: Session
    ) -> AvailabilityModel:
        provider = ProviderService._get_provider_for_user(user_id, db)
        availability = (
            db.query(AvailabilityModel)
            .filter(
                AvailabilityModel.id == availability_id,
                AvailabilityModel.provider_id == provider.id,
            )
            .first()
        )
        if availability is None:
            raise HTTPException(status_code=404, detail="Availability record not found")
        return availability

    @staticmethod
    def update_my_availability(
        user_id: str,
        availability_id: str,
        data: AvailabilityUpdateReq,
        db: Session,
    ):
        availability = ProviderService._get_my_availability_record(
            user_id, availability_id, db
        )
        updates = {
            field: value
            for field, value in data.model_dump(exclude_unset=True).items()
            if value is not None
        }
        start_time = updates.get("start_time", availability.start_time)
        end_time = updates.get("end_time", availability.end_time)
        if end_time <= start_time:
            raise HTTPException(
                status_code=422,
                detail="end_time must be later than start_time",
            )
        if "location_id" in updates:
            location = (
                db.query(LocationsModel)
                .filter(
                    LocationsModel.id == updates["location_id"],
                    LocationsModel.is_active.is_(True),
                )
                .first()
            )
            if location is None:
                raise HTTPException(status_code=404, detail="Active location not found")

        for field, value in updates.items():
            setattr(availability, field, value)
        db.commit()
        db.refresh(availability)
        return {
            "status": 200,
            "message": "Provider availability updated successfully",
            "data": availability,
        }

    @staticmethod
    def delete_my_availability(user_id: str, availability_id: str, db: Session):
        availability = ProviderService._get_my_availability_record(
            user_id, availability_id, db
        )
        availability_data = AvailabilityData.model_validate(availability)
        db.delete(availability)
        db.commit()
        return {
            "status": 200,
            "message": "Provider availability deleted successfully",
            "data": availability_data,
        }
