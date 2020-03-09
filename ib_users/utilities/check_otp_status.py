def check_otp_status(ib_user, otp_details):
    otp_count = otp_details.otp_count

    import datetime
    time_now = datetime.datetime.now()
    time_delta = datetime.timedelta(hours=24)

    if otp_details.creation_datetime + time_delta <= time_now:
        otp_details.otp_count = 0
        otp_details.save()

    from django.conf import settings
    if otp_count >= settings.OTP_LIMIT:
        res_status = "OTP_LIMITED_EXCEEDED"
        otp_left = 0
    else:
        otp_count += 1
        otp_left = int(settings.OTP_LIMIT) - otp_count

        from ib_users.utilities.generate_otp import generate_otp
        username = ib_user.username
        otp = generate_otp(username)

        from ib_users.utilities.send_sms import send_sms
        send_sms(mobile_numbers=[username], message='OTP for K Feed is '+str(otp), message_type='N', sender_id='KOSSIP')
        print "otp--->", otp

        otp_details.otp_count = otp_count
        ib_user.set_password(otp)
        ib_user.save()
        otp_details.save()
        res_status = "OTP_SENT"

    return res_status, otp_left
