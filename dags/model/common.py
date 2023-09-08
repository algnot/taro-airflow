from datetime import datetime, timedelta


def get_next_datetime_schedule_by_schedule(schedule):
    now = datetime.now()
    schedule = schedule.split(" ")
    next_datetime = now + timedelta(seconds=1)
    if schedule[0] != "*":
        next_datetime = next_datetime.replace(second=0)
        next_datetime = next_datetime + timedelta(minutes=1)
    if schedule[1] != "*":
        next_datetime = next_datetime.replace(minute=0)
        next_datetime = next_datetime + timedelta(hours=1)
    if schedule[2] != "*":
        next_datetime = next_datetime.replace(hour=0)
        next_datetime = next_datetime + timedelta(days=1)
    if schedule[3] != "*":
        next_datetime = next_datetime.replace(day=1)
        next_datetime = next_datetime + timedelta(weeks=1)
    if schedule[4] != "*":
        next_datetime = next_datetime.replace(month=1)
        next_datetime = next_datetime + timedelta(years=1)
    return next_datetime

