from fastapi import HTTPException
from app.schemas.auth_schemas import LoginReq, RegisterReq
from sqlalchemy.orm import Session
from app.models.users_models import UsersModel
from app.core.security import verify_password, hash_password, create_token


class AuthService:
    @staticmethod
    def register_user(data: RegisterReq, db: Session):
        password_hash = hash_password(data.password)

        new_user = UsersModel(**data.model_dump())
        new_user.password = password_hash

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "status": 201,
            "message": "User added successfully",
            "data": new_user,
        }

    @staticmethod
    def login_user(data: LoginReq, db: Session):
        check_user = db.query(UsersModel.email == data.email).first()
        if not check_user:
            raise HTTPException(
                status_code=404, detail=f"User not found with {data.email}"
            )

        valid_password = verify_password(data.password, check_user.password)

        if not valid_password:
            raise HTTPException(status_code=400, detail=f"Bad credentials")

        return {"status": 200, "message": "Loggedin successfully", "data": check_user}
