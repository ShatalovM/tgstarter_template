import sys
from typing import NoReturn

from aiogram.dispatcher.handler import SkipHandler
from aiogram import types

from preparation import (
    config,
    logger,
    bot,
    dispatcher as dp
)


@dp.any_update_handler()
async def log_update(update: types.Update) -> NoReturn:
    await logger.info(update=update)
    raise SkipHandler


@dp.state_handler(bound=dp.errors_handler)
async def log_error(update: types.Update, error: Exception) -> bool:
    text = await logger.error(update=update, exc_info=sys.exc_info())
    await bot.send_message(
        chat_id=config.bot.error_chat_id,
        text=text
    )
    return True  # for aiogram
