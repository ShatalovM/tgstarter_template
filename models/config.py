from typing import Optional, List

import pytz
from pydantic import BaseModel, validator
# from aiogram.types import ParseMode


class BotConfig(BaseModel):

    @validator('timezone', pre=True)
    def timezone_validator(cls, zone: str) -> pytz.tzinfo.DstTzInfo:
        return pytz.timezone(zone)

    class Config:
        arbitrary_types_allowed = True

    token: str
    proxy: Optional[str]
    parse_mode: str
    states_dir: str
    timezone: pytz.tzinfo.DstTzInfo


class MongoConfig(BaseModel):
    uri: str
    dbname: str
    collections: List[str]


class BaseConfig(BaseModel):
    bot: BotConfig
    mongo: MongoConfig
