from aiogram import executor

from preparation import dispatcher


if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher)
