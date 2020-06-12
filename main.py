import logging

from aiogram import executor

from preparation import dispatcher
import states


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dispatcher=dispatcher)
