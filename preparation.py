from aiogram import Bot
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import yaml

from tgstarter import Dispatcher, MongoStorage

from models.config import BaseConfig
from tgstarter.utils import yaml_tools, helper


CONFIG_PATH = 'settings/config.yaml'
YAMLS = yaml_tools.load_yamls(
    CONFIG_PATH,
    loader=yaml.SafeLoader
)

config = BaseConfig(**YAMLS[CONFIG_PATH])


jinja2_env = jinja2.Environment(autoescape=True)
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
