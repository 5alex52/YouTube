from ..dao import BaseDAO
from .models import UserTagsModel
from .schemas import UserTagsCreate
from .schemas import UserTagsUpdate


class UserTagsModelDAO(BaseDAO[UserTagsModel, UserTagsCreate, UserTagsUpdate]):
    model = UserTagsModel
