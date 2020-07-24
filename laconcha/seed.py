import string
from random import choices


def get_seed():
    return ''.join(choices(string.hexdigits, k=32))


class Seed:
    pass
