import argparse

from . import weights

def run():
    parser = argparse.ArgumentParser(description='BroBot: A workout helper.')
    subcommands = parser.add_subparsers(dest='command', required=True)
    weights_parser = subcommands.add_parser(
        'weights',
        parents=[weights.parser],
        description=weights.parser.description,
        help='Compute the plates needed for two weight targets.',
    )
    weights_parser.set_defaults(func=lambda args: weights.main(args.t1, args.t2))
    args = parser.parse_args()
    args.func(args)
