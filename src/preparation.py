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
from tgstarter.middlewares.state_switch import StateSwitch
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
YAML_FILES = yaml_tools.load_yaml_files(CONFIG_PATH, loader=yaml.SafeLoader)

config = BaseConfig(**YAML_FILES[CONFIG_PATH])


jinja2_env = jinja2.Environment(autoescape=True)
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

dispatcher = Dispatcher(bot=bot, storage=storage)
STATE_SWITCH = StateSwitch(storage=storage)
dispatcher.middleware.setup(STATE_SWITCH)

scheduler = AsyncIOScheduler(timezone=config.bot.timezone)
