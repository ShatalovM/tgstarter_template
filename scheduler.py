import asyncio
from datetime import datetime
import calendar

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from preparation import scheduler


def main() -> None:
    scheduler.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()


@scheduler.scheduled_job(DateTrigger(run_date=datetime.now()))
async def date_job() -> None:
    print('USELESS JOB')


@scheduler.scheduled_job(CronTrigger(day_of_week=calendar.MONDAY, hour=8, minute=0))
async def cron_job() -> None:
    print('ULTIMATE NOTIFICATION')


@scheduler.scheduled_job(IntervalTrigger(seconds=10))
async def interval_job() -> None:
    print('10 SECONDS HAVE PASSED')


if __name__ == '__main__':
    main()
