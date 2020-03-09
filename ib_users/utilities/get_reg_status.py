def get_reg_status(username):

    from ib_users.models.ib_user import IBUser
    try:
        IBUser.objects.get(username=username)
        return "REGISTERED"
    except:
        return "NOT_REGISTERED"
