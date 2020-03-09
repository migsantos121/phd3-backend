__author__ = 'vedavidh'


def convert_datetime_to_string(obj, format_="%b %d, %Y at %I:%M%p"):
    try:
        datetime_str = obj.strftime(format=format_)
    except:
        return None
    return datetime_str
