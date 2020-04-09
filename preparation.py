from aiogram import Bot
import jinja2
from motor.motor_asyncio import AsyncIOMotorClient
import yaml
import addict

from tgstarter import Dispatcher, MongoStorage

from models.config import BaseConfig
from utils import yaml_tools


jinja2_env = jinja2.Environment(autoescape=True)


yaml.add_constructor(
    tag='!Template',
    constructor=yaml_tools.get_template_constructor(
        jinja2_env=jinja2_env),
    Loader=yaml.SafeLoader
)


CONFIG_PATH = 'settings/config.yaml'
CONTENT_PATH = 'settings/content.yaml'
YAMLS = yaml_tools.load_yamls(
    CONFIG_PATH,
    CONTENT_PATH,
    loader=yaml.SafeLoader
)

config = BaseConfig(**YAMLS[CONFIG_PATH])
content = addict.Dict(YAMLS[CONTENT_PATH])


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
