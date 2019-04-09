#! python
import asyncio
import argparse
import logging

logger = logging.getLogger('Crizzle')
logging.basicConfig(level=logging.INFO)


async def record(args):
    while True:
        pass


async def test(args):
    pass


async def live(args):
    pass


parser = argparse.ArgumentParser('Crizzle')
parser.add_argument('--logdir', default='../logs')
subparsers = parser.add_subparsers(dest='mode', required=True)

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


async def main(args):
    return await args.func(args)


if __name__ == '__main__':
    logger.info(f"Running Crizzle in mode {arguments.mode}")
    asyncio.run(main(arguments))
