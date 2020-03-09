def generate_otp(username):
    from otpauth import OtpAuth
    auth = OtpAuth(username)
    otp = auth.totp(period=1)
    return otp
