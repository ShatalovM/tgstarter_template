import logging
from typing import NoReturn

from aiogram import executor

from src.preparation import dispatcher
import src.states  # noqa


def main() -> NoReturn:
    logging.basicConfig(level=logging.DEBUG)
    executor.start_polling(dispatcher=dispatcher)

# if __name__ == '__main__':
#     logging.basicConfig(level=logging.DEBUG)
#     executor.start_polling(dispatcher=dispatcher)
