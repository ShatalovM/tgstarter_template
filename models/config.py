from typing import Optional, List
from enum import auto

from pydantic import BaseModel
from tgstarter.utils.helper import NamedEnum


class ParseMode(str, NamedEnum):
    HTML = auto()
    Markdown = auto()


class BotConfig(BaseModel):
    token: str
    proxy: Optional[str]
    parse_mode: ParseMode
    states_dir: str


class MongoConfig(BaseModel):
    uri: str
    dbname: str
    collections: List[str]


class BaseConfig(BaseModel):
    bot: BotConfig
    mongo: MongoConfig
