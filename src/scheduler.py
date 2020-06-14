import asyncio
import calendar
from datetime import datetime
import logging

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from src.preparation import scheduler, config


timezone = config.bot.timezone


def main() -> None:
    scheduler.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()


@scheduler.scheduled_job(DateTrigger(timezone=timezone, run_date=datetime.now()))
async def date_job() -> None:
    print('USELESS JOB')


@scheduler.scheduled_job(CronTrigger(timezone=timezone, day_of_week=calendar.MONDAY, hour=8, minute=0))
async def cron_job() -> None:
    print('ULTIMATE NOTIFICATION')


@scheduler.scheduled_job(IntervalTrigger(timezone=timezone, seconds=10))
async def interval_job() -> None:
    print('10 SECONDS HAVE PASSED')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
