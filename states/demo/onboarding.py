from aiogram.types import Message
from django import forms

from preparation import dispatcher as dp
# import settings.content as content
from settings import content


EMAIL_FIELD = forms.EmailField()


@dp.state_handler(primary_state=True, bound=dp.message_handler)
async def greeting(msg: Message):
    await msg.answer(
        text=content.onboarding.greeting.render(
            first_name=msg.from_user.first_name
        )
    )
    return user_email


@dp.state_handler(bound=dp.message_handler)
async def user_email(msg: Message):
    try:
        EMAIL_FIELD.clean(msg.text)
    except forms.ValidationError:
        await msg.answer(content.onboarding.user_email__error)
    else:
        await msg.answer(content.onboarding.user_email__success)
        # here must be logic to save the email somewhere :)
        return dummy_state


@dp.state_handler(bound=dp.message_handler)
async def dummy_state(msg: Message):
    await msg.answer(
        text=content.onboarding.test_inline_markup__text,
        reply_markup=content.onboarding.test_inline_markup__keyboard
    )
    await msg.answer(
        text=content.onboarding.test_reply_markup__text,
        reply_markup=content.onboarding.test_reply_markup__keyboard
    )
