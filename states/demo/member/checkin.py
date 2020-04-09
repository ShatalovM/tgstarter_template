from typing import Any, Optional, Callable

from aiogram.types import Message

from preparation import dispatcher as dp
import states.demo.admin


@dp.state_handler(bound=dp.message_handler)
async def checkin_menu(message: Message) -> Optional[Callable[..., Any]]:
    await message.answer('STATE-3')
    return states.demo.admin.admin_menu
