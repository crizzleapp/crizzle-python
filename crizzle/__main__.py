import argparse


def record(args):
    pass


def test(args):
    pass


def live(args):
    pass


parser = argparse.ArgumentParser('Crizzle')
subparsers = parser.add_subparsers(dest='mode')

# Data Recording-Only mode
record_parser = subparsers.add_parser('record')
record_parser.set_defaults(func=record)

# Testing mode
test_parser = subparsers.add_parser('test')
test_parser.set_defaults(func=test)

# Live Trading mode
live_parser = subparsers.add_parser('live')
live_parser.set_defaults(func=live)

arguments = parser.parse_args()


def main(args):
    return args.func(args)


if __name__ == '__main__':
    main(arguments)
