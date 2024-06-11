from typing import Optional
from jose import jwt
from .config import settings
from .exceptions import InvalidTokenException
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import status, Request


def get_user_id(request: Request):
    return verify_token(request)

def verify_token(request: Request, token: Optional[str] = None) -> Optional[str]:
    if token is None:
        token = get_token(request)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException
    except Exception:
        raise InvalidTokenException
    return user_id

def get_token(request: Request, auto_error = True):
    authorization: str = request.cookies.get("access_token")

    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        if auto_error:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return None
    return param