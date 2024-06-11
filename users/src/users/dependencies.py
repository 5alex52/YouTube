import uuid
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from .models import UserModel
from .service import UserService
from .utils import OAuth2PasswordBearerWithCookie
from ..global_utils import verify_token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[UserModel]:
    user_id = verify_token(None, token)
    current_user = await UserService.get_user(uuid.UUID(user_id))
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Verify email"
        )
    return current_user


async def get_current_superuser(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges"
        )
    return current_user


async def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not active"
        )
    return current_user
