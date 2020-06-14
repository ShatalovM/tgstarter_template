from aiogram.utils.exceptions import (
    BotBlocked,
    ChatNotFound,
    RetryAfter,
    UserDeactivated,
    TelegramAPIError,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from motor.motor_asyncio import AsyncIOMotorClient
import jinja2
import yaml

from tgstarter import Bot, Dispatcher, MongoStorage, MongoLogger
from tgstarter.utils import jinja2_filters
from tgstarter.utils.content import ContentValidator
from tgstarter.utils import yaml_tools, helper

from src.models.config import BaseConfig


ANY_STATE = '*'
TEXT_MESSAGE_LIMIT = 4096
BROADCAST_EXCEPTIONS = (
    BotBlocked,
    ChatNotFound,
    RetryAfter,
    UserDeactivated,
    TelegramAPIError,
)


CONFIG_PATH = 'src/settings/config.yaml'
YAMLS = yaml_tools.load_yamls(
    CONFIG_PATH,
    loader=yaml.SafeLoader
)

config = BaseConfig(**YAMLS[CONFIG_PATH])


jinja2_env = jinja2.Environment(autoescape=True)
jinja2_env.filters['fullname'] = jinja2_filters.fullname_jinja2_filter
template = helper.get_template_function(jinja2_env=jinja2_env)


validator = ContentValidator(
    delete_indentation=helper.delete_indentation,
    create_jinja2_template=jinja2_env.from_string,
)
validated_class = validator.validated_class


MONGO_CLIENT = AsyncIOMotorClient(config.mongo.uri)
storage = MongoStorage(
    mongo_client=MONGO_CLIENT,
    mongo_database=MONGO_CLIENT[config.mongo.dbname],
)

MONGO_LOGGING_CLIENT = AsyncIOMotorClient(config.mongo.logging.uri)
logger = MongoLogger(
    mongo_client=MONGO_LOGGING_CLIENT,
    mongo_database=MONGO_LOGGING_CLIENT[config.mongo.logging.dbname],
    collection_name=config.mongo.logging.collection,
    timezone=config.bot.timezone,
    message_format=template(config.mongo.logging.message_format),
)


bot = Bot(
    token=config.bot.token,
    proxy=config.bot.proxy,
    parse_mode=config.bot.parse_mode,
)

dispatcher = Dispatcher(
    states_dir=config.bot.states_dir,
    bot=bot,
    storage=storage,
)


scheduler = AsyncIOScheduler(timezone=config.bot.timezone)
