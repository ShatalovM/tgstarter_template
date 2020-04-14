from aiogram import Bot
from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    RetryAfter,
    UserDeactivated,
    TelegramAPIError,
)
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tgstarter import Dispatcher, MongoStorage
from tgstarter.utils import jinja2_filters

from models.config import BaseConfig
from tgstarter.utils import yaml_tools, helper


ANY_STATE = '*'
TEXT_MESSAGE_LIMIT = 4096
BROADCAST_EXCEPTIONS = (
    BotBlocked,
    ChatNotFound,
    RetryAfter,
    UserDeactivated,
    TelegramAPIError,
)


CONFIG_PATH = 'settings/config.yaml'
YAMLS = yaml_tools.load_yamls(
    CONFIG_PATH,
    loader=yaml.SafeLoader
)

config = BaseConfig(**YAMLS[CONFIG_PATH])


jinja2_env = jinja2.Environment(autoescape=True)
jinja2_env.filters['fullname'] = jinja2_filters.fullname_jinja2_filter
template = helper.get_template_function(jinja2_env=jinja2_env)


bot = Bot(
    token=config.bot.token,
    proxy=config.bot.proxy,
    parse_mode=config.bot.parse_mode,
)

mongo_client = AsyncIOMotorClient(config.mongo.uri)
storage = MongoStorage(
    mongo_client=mongo_client,
    mongo_database=mongo_client[config.mongo.dbname]
)

dispatcher = Dispatcher(
    states_dir=config.bot.states_dir,
    bot=bot,
    storage=storage,
)

scheduler = AsyncIOScheduler(timezone=config.bot.timezone)
