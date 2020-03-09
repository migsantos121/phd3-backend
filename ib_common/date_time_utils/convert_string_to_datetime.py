"""
Created on 13/04/17

@author: revanth
"""


def convert_string_to_date_time(string, format_="%b %d, %Y at %I:%M%p"):
    """ 
        Default Datetime format : 'Aug 09, 2015 at 11:09PM'
    """
    from datetime import datetime

    try:
        datetime_object = datetime.strptime(string, format_)
    except:
        datetime_object = None
    return datetime_object
