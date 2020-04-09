from typing import Any, Optional, Callable

from aiogram.types import Message

from preparation import dispatcher as dp
import states.demo.member.event.registration


@dp.state_handler(primary_state=True, bound=dp.message_handler)
async def admin_menu(message: Message) -> Optional[Callable[..., Any]]:
    await message.answer('STATE-1')
    return states.demo.member.event.registration.registration_menu
