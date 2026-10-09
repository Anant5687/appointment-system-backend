import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.roles_models import RolesModel
from app.models.users_models import UsersModel
from app.core.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> UsersModel:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authentication token required")

    try:
        payload = decode_token(credentials.credentials)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    user = db.query(UsersModel).filter(UsersModel.id == user_id).first()
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid or inactive user")

    return user


def get_admin_user(
    user: UsersModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UsersModel:
    role = db.query(RolesModel).filter(RolesModel.id == user.role_id).first()
    if role is None or role.name.upper() != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user
