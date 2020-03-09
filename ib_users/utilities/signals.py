__author__ = 'tanmay.ibhubs'

import django.dispatch

ib_user_registered_signal = django.dispatch.Signal()
ib_user_registration_verification_signal = django.dispatch.Signal()
ib_user_logout_signal = django.dispatch.Signal()
ib_user_activated_signal = django.dispatch.Signal()
