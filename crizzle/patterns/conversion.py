from decimal import Decimal, Context


def float_to_str(inp):
    context = Context()
    context.prec = 20
    dec = context.create_decimal(repr(inp))
    return format(dec, 'f')
