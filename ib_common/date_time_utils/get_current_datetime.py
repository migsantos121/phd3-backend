__author__ = 'vedavidh'


def get_current_datetime():
    import datetime
    from django.utils.timezone import utc

    now = datetime.datetime.utcnow().replace(tzinfo=utc)

    return now
