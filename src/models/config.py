from typing import Optional, List

import pytz
from pydantic import BaseModel, validator


class BotConfig(BaseModel):

    @validator('timezone', pre=True)
    def timezone_validator(cls, zone: str) -> pytz.tzinfo.DstTzInfo:
        return pytz.timezone(zone)

    class Config:
        arbitrary_types_allowed = True

    token: str
    proxy: Optional[str]
    parse_mode: str
    timezone: pytz.tzinfo.DstTzInfo
    error_chat_id: int


class MongoLogging(BaseModel):
    uri: str
    dbname: str
    collection: str
    message_format: str


class MongoConfig(BaseModel):
    uri: str
    dbname: str
    collections: List[str]
    logging: MongoLogging


class BaseConfig(BaseModel):
    bot: BotConfig
    mongo: MongoConfig
