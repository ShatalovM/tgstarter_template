from aiogram.types import Message
from django import forms

from preparation import dispatcher as dp, content


EMAIL_FIELD = forms.EmailField()


@dp.state_handler(primary_state=True, bound=dp.message_handler)
async def greeting(msg: Message):
    await msg.answer(content.msg.greeting.render(first_name=msg.from_user.first_name))
    return user_email


@dp.state_handler(bound=dp.message_handler)
async def user_email(msg: Message):
    try:
        EMAIL_FIELD.clean(msg.text)
    except forms.ValidationError:
        await msg.answer(content.msg.user_email.error)
    else:
        await msg.answer(content.msg.user_email.success)
        # here must be logic to save the email somewhere :)
        return dummy_state


@dp.state_handler(bound=dp.message_handler)
async def dummy_state(msg: Message):
    await msg.answer(
        text=content.msg.test_inline_keyboard.text,
        reply_markup=content.msg.test_inline_keyboard.inline_keyboard
    )
    await msg.answer(
        text=content.msg.test_reply_markup.text,
        reply_markup=content.msg.test_reply_markup.reply_markup
    )
