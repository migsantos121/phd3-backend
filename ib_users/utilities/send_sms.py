from enum import Enum


class DeliveryReport(Enum):
    required = "Y"
    notRequired = "N"


class MessageType(Enum):
    normal = "N"


class SenderIdType(Enum):
    kossip = "KOSSIP"
    ibuild = "IBUILD"
    makeit = "MAKEIT"
    ibinfo = "IBINFO"
    cyberi = "CYBERI"
    englsh = "ENGLSH"
    ispeak = "ISPEAK"
    ibsafe = "IBSAFE"


def is_null_or_empty(field_name):
    if field_name is not None and field_name.strip() != "":
        return False
    return True


def get_ascii_string(char_sequence):
    if type(char_sequence) != int:
        if is_null_or_empty(char_sequence) or len(char_sequence) == 0:
            return ''
        return ''.join([i if ord(i) < 128 else '' for i in char_sequence])
    else:
        return char_sequence


def send_sms(mobile_numbers, message, message_type=None, sender_id=None):
    import urllib2
    import urllib
    from django.conf import settings

    if message_type is None:
        message_type = MessageType.normal.value

    if sender_id is None:
        sender_id = settings.SMSCOUNTRY_DEFAULT_SENDER_ID

    mobile_numbers = ','.join(mobile_numbers)
    delivery_report_value = DeliveryReport.required.value

    message = get_ascii_string(message)
    message = message.strip()

    params = {'message': message, 'mtype': message_type, 'dr': delivery_report_value,
              'User': settings.SMSCOUNTRY_USERNAME, 'passwd': settings.SMSCOUNTRY_PASSWORD,
              'mobilenumber': mobile_numbers, 'sid': sender_id}

    print "Send OTP Params ---> ", params
    encoded_params = urllib.urlencode(params)

    uri = "http://api.smscountry.com/SMSCwebservice_bulk.aspx?" + encoded_params

    try:
        print urllib2.urlopen(uri).read()
    except Exception as e:
        print "Send OTP Error ---> ", e
        pass

    return
