__author__ = 'anush0247'


def generate_id(size):
    import string
    import random
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))
