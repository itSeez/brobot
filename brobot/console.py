import argparse

from . import weights

def run():
    parser = argparse.ArgumentParser(description='BroBot: A workout helper.')
    parser.add_argument(dest='command', choices=['weights'], help='BroBot command.')
    parser.add_argument('vars', nargs='*', help='Command arguments.')
    args = parser.parse_args()

    match args.command:
        case 'weights':
            if len(args.vars) == 2:
                t1 = int(args.vars[0])
                t2 = int(args.vars[1])
                weights.main(t1, t2)
            else:
                weights.parser.print_help()
                return
        case _:
            parser.print_usage()
