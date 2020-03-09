__author__ = 'vedavidh'


def convert_datetime_to_local_string(obj, format_="%b %d, %Y at %I:%M%p"):
    import pytz
    try:
        tz = pytz.timezone("Asia/Calcutta")
        if obj.tzinfo is None:
            obj = obj.replace(tzinfo=pytz.UTC)
        obj = tz.normalize(obj)
        datetime_str = obj.strftime(format=format_)
    except:
        return None
    return datetime_str
