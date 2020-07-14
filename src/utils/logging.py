import sys
from typing import Callable, Optional, Any
import functools

from aiogram import types
from tgstarter.models import storage as models
from tgstarter.utils.typing import ExcInfo
from tgstarter.utils.helper import function_fullname

from src.preparation import config, logger, bot


async def log_event(
    level: models.LogLevel,
    type: Optional[models.LogType] = None,
    update: Optional[types.Update] = None,
    task: Optional[models.LogTask] = None,
    from_bot: bool = False,
    exc_info: Optional[ExcInfo] = None,
) -> types.Message:
    text = await logger.log(
        level=level,
        type=type,
        update=update,
        task=task,
        from_bot=from_bot,
        exc_info=exc_info
    )
    return await bot.send_large_message(chat_id=config.bot.error_chat_id, text=text)


def task_logger(
    positive_level: models.LogLevel = models.LogLevel.INFO,
    negative_level: models.LogLevel = models.LogLevel.ERROR,
    type: models.LogType = models.LogType.TASK,
    from_bot: bool = False,
) -> Callable:

    def decorator(callback: Callable) -> Callable:
        @functools.wraps(callback)
        async def wrapper(*args, **kwargs) -> Any:
            task = models.LogTask(
                function_fullname=function_fullname(callback),
                args=args,
                kwargs=kwargs
            )

            try:
                callback_result = await callback(*args, **kwargs)
            except Exception:
                text = await logger.log(
                    task=task,
                    level=negative_level,
                    type=type,
                    from_bot=from_bot,
                    exc_info=sys.exc_info()
                )
                await bot.send_large_message(chat_id=config.bot.error_chat_id, text=text)
            else:
                task.result = callback_result
                await logger.log(
                    task=task,
                    level=positive_level,
                    type=type,
                    from_bot=from_bot
                )
                return callback_result

        return wrapper
    return decorator
