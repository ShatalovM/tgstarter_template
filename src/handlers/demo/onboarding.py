from aiogram.types import Message, ReplyKeyboardRemove
from django import forms

from src.preparation import dispatcher as dp, ANY_STATE
from src.settings import content
from src.utils.constants import State


EMAIL_FIELD = forms.EmailField()


@dp.message_handler()
@dp.message_handler(commands='start', state=ANY_STATE)
async def greeting(msg: Message):
    await msg.answer(
        text=content.onboarding.greeting.text.render(
            first_name=msg.from_user.first_name
        ),
        reply_markup=ReplyKeyboardRemove()
    )
    return State.USER_EMAIL


@dp.message_handler(state=State.USER_EMAIL)
async def user_email(msg: Message):
    try:
        EMAIL_FIELD.clean(msg.text)
    except forms.ValidationError:
        await msg.answer(content.onboarding.user_email.invalid)
    else:
        await msg.answer(content.onboarding.user_email.valid)
        # here must be logic to save the email somewhere :)
        return State.DUMMY_STATE


@dp.message_handler(state=State.DUMMY_STATE)
async def dummy_state(msg: Message):
    await msg.answer(
        text=content.onboarding.test_inline_keyboard.text,
        reply_markup=content.onboarding.test_inline_keyboard.reply_markup
    )
    await msg.answer(
        text=content.onboarding.test_keyboard.text,
        reply_markup=content.onboarding.test_keyboard.reply_markup
    )
