__author__ = 'vedavidh'


def get_current_local_date_time():
    import datetime, pytz
    from django.utils.timezone import utc
    tz = pytz.timezone("Asia/Calcutta")
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    now = tz.normalize(now)
    return now
