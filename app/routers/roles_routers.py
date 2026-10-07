from app.services.roles_services import RolesService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.roles_schemas import RolesReq, RolesRes, AllRolesRes

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/all", response_model=AllRolesRes)
def all_roles(db: Session = Depends(get_db)):
    try:
        return RolesService.get_all_roles(db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.post("/create", response_model=RolesRes)
def create_role(data: RolesReq, db: Session = Depends(get_db)):
    try:
        return RolesService.create_role(data, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )


@router.delete("/user_id/{user_id}/role_id/{role_id}", response_model=RolesRes)
def delete_role(user_id: str, role_id: str, db: Session = Depends(get_db)):
    try:
        return RolesService.delete_role(user_id, role_id, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"{str(e) or "Internal server error"}"
        )
