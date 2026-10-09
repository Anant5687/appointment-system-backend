import jwt
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from app.core.settings import settings

password_hash = PasswordHash.recommended()

def hash_password(plain_pass: str):
    return password_hash.hash(plain_pass)

def verify_password(plain_pass: str, hash_pass: str):
    return password_hash.verify(plain_pass, hash_pass)

def create_token(user_id: str):
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_TOKEN_EXPIRE
    )

    payload = {"sub": user_id, "exp": expires_at}

    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHIM
    )

    return token


def decode_token(token: str):
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHIM],
    )
