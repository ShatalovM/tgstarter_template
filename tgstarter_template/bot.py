from aiogram import executor

from tgstarter_template.preparation import dispatcher


if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher)
