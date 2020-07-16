import logging
from typing import NoReturn

from aiogram import executor

from src.preparation import dispatcher
import src.handlers  # noqa


def main() -> NoReturn:
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dispatcher=dispatcher)
