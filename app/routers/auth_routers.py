from app.services.auth_services import AuthService
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import LoginReq, LoginRes, RegisterRes, RegisterReq
from app.db.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=RegisterRes)
def user_register(data: RegisterReq, db: Session = Depends(get_db)):
    try:
        return AuthService.register_user(data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.post("/login", response_model=LoginRes)
def login_uset(data: LoginReq, db: Session = Depends(get_db)):
    try:
        return AuthService.login_user(data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
