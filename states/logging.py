import sys
from typing import NoReturn

from aiogram.dispatcher.handler import SkipHandler
from aiogram import types
from tgstarter.models.storage import LogLevel, LogType

from utils.logging import log_event
from preparation import logger, dispatcher as dp


@dp.any_update_handler()
async def log_update(update: types.Update) -> NoReturn:
    await logger.info(update=update)
    raise SkipHandler


@dp.errors_handler()
async def log_error(update: types.Update, error: Exception) -> bool:
    await log_event(
        update=update,
        level=LogLevel.ERROR,
        type=LogType.EVENT,
        exc_info=sys.exc_info()
    )
    return True  # for aiogram
