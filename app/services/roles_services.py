from sqlalchemy.orm import Session
from app.schemas.roles_schemas import RolesReq
from app.models.roles_models import RolesModel
from app.models.users_models import UsersModel
from fastapi import HTTPException


class RolesService:

    @staticmethod
    def get_all_roles(db: Session):
        return {
            "status": 200,
            "message": "Roles data",
            "data": db.query(RolesModel).all(),
        }

    @staticmethod
    def create_role(data: RolesReq, db: Session):
        new_role = RolesModel(**data.model_dump())
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return {"status": 201, "message": "Role added succesfully", "data": new_role}

    @staticmethod
    def remove_role(user_id: str, role_id: str, db: Session):
        check_user = db.query(UsersModel).filter(UsersModel.id == user_id).first()

        if not check_user:
            raise HTTPException(
                status_code=404, detail=f"User not found with {user_id}"
            )

        check_role = db.query(RolesModel).filter(RolesModel.id == role_id).first()

        if not check_role:
            raise HTTPException(
                status_code=404, detail=f"Role not found with {role_id}"
            )

        if check_role.name != "ADMIN":
            raise HTTPException(status_code=422, detail="Do not have permission")

        return {
            "status": 200,
            "message": "Role deleted successfully",
            "data": check_role,
        }
