from aiogram.types import (
    KeyboardButton as Button,
    InlineKeyboardButton as InlineButton,
)
from jinja2 import Template
from tgstarter.utils.helper import (
    ReplyKeyboardMarkup as Keyboard,
    InlineKeyboardMarkup as InlineKeyboard,
)

from src.preparation import validated_class


@validated_class
class greeting:
    text: Template = '''
    Hello {{ first_name }} 🙂
    Please send your FAKE email for nothing.
    '''


@validated_class
class user_email:
    valid = '''
    Thanks, I saved it.
    Text me something.
    '''

    invalid = '''
    Sorry, the email is invalid.
    Please enter it again.
    '''


class test_keyboard:
    text = 'Send it again?'
    reply_markup = Keyboard(
        [
            Button('Yes'),
            Button('Sure'),
        ],
        Button(
            text='Give contact',
            request_contact=True
        )
    )


class test_inline_keyboard:
    class callbacks:
        option1 = 'OPTION-1'
        option2 = 'OPTION-2'
        option3 = 'OPTION-3'

    text = 'Inline keyboard test'
    reply_markup = InlineKeyboard(
        [
            InlineButton(
                text='Option-1',
                callback_data=callbacks.option1
            ),
            InlineButton(
                text='Option-2',
                callback_data=callbacks.option2
            ),
        ],
        InlineButton(
            text='Separated button',
            callback_data=callbacks.option3
        )
    )
