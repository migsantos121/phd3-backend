def reset_otp_count(ib_user):
    from ib_users.models.otp_details import OTPDetails
    ib_user_otp_details = OTPDetails.objects.get(ib_user=ib_user)
    ib_user_otp_details.otp_count = 0
    ib_user_otp_details.save()
