from aiogram.types import (
    KeyboardButton as Button,
    InlineKeyboardButton as InlineButton,
)
from tgstarter.utils.helper import (
    ReplyKeyboardMarkup as Keyboard,
    InlineKeyboardMarkup as InlineKeyboard,
)

from preparation import template


greeting = template('''
    Hello {{ first_name }} 🙂
    Please send your FAKE email for nothing.
''')


user_email__success = 'Thanks, I saved it.'
user_email__error = '''
Sorry, the email is invalid.
Please enter it again.
'''


test_reply_markup__text = 'Send it again?'
test_reply_markup__keyboard = Keyboard(
    [
        'Yes',
        'Sure'
    ],
    Button(
        text='Give contact',
        request_contact=True
    )
)


test_inline_markup__text = 'Inline keyboard test'
test_inline_markup__option1 = 'OPTION-1'
test_inline_markup__option2 = 'OPTION-2'
test_inline_markup__keyboard = InlineKeyboard(
    [
        InlineButton(
            text='Option-1',
            callback_data=test_inline_markup__option1
        ),
        InlineButton(
            text='Option-2',
            callback_data=test_inline_markup__option2
        ),
    ],
    InlineButton(
        text='Separated button',
        callback_data='SOME_CALLBACK'
    )
)
