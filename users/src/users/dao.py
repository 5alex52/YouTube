from ..dao import BaseDAO
from .models import RefreshSessionModel
from .models import UserModel
from .schemas import RefreshSessionCreate
from .schemas import RefreshSessionUpdate
from .schemas import UserCreateDB
from .schemas import UserUpdateDB


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel


class RefreshSessionDAO(
    BaseDAO[RefreshSessionModel, RefreshSessionCreate, RefreshSessionUpdate]
):
    model = RefreshSessionModel
