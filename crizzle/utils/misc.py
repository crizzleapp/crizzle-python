import random
import string
from decimal import Decimal, Context


def float_to_str(inp):
    context = Context()
    context.prec = 20
    dec = context.create_decimal(repr(inp))
    return format(dec, 'f')


def random_string(length=4):
    letters = string.ascii_lowercase + string.digits
    chosen_letters = [random.choice(letters) for _ in range(length)]
    return ''.join(chosen_letters)
