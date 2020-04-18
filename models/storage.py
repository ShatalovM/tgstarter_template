from typing import (
    Optional,
    Dict,
    Any,
    Union,
)

from pydantic import (
    BaseModel,
    validator,
    Field,
)
from bson.objectid import ObjectId
from tgstarter.utils.helper import FlagEnum, auto
from utils.typing import UserId, ChatId


class MongoObject(BaseModel):
    id: Optional[ObjectId] = Field(None, alias='_id')

    @validator('id', pre=True, always=True)
    def validate_object_id(cls, value: Any) -> ObjectId:
        if isinstance(value, ObjectId) or value is None:
            return value
        else:
            raise ValueError('field _id must be of type ObjectId')

    class Config:
        arbitrary_types_allowed = True
        # use_enum_values = True


class UserFlag(str, FlagEnum):
    MATCHING_WAITING = auto()
    MATCHED = auto()


class UserVar(str, FlagEnum):
    reserved_state = auto()


class TelegramUser(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]


class UserRights(str, FlagEnum):
    ADMIN = auto()
    MEMBER = auto()


class UserData(BaseModel):
    # TODO: replace all Dict objects with addict.Dict
    class Config:
        use_enum_values = True

    rights: Optional[Union[UserRights, str]]
    telegram_entity: Optional[TelegramUser]
    # str is needed for type checker
    flags: Optional[Dict[Union[UserFlag, str], Any]]
    vars: Optional[Dict[Union[UserVar, str], Any]]


class User(MongoObject):
    user_id: Optional[UserId]
    chat_id: Optional[ChatId]
    state: Optional[str]
    userdata: Optional[UserData]
    state_data: Optional[Dict[Any, Any]]
