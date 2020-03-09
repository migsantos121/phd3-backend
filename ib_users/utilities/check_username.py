def check_username(username):
    try:
        int(username)
        return True
    except:
        return False
