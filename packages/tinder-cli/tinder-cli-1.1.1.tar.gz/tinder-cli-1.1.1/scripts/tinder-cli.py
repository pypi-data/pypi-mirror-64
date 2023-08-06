#!/usr/bin/env python3

import re
import sys
import getpass
import argparse

import requests

from tinder_cli.cli import TinderCLI


def main():
    args = parse_args()
    tinder_token = TinderCLI.get_tinder_token(args.token)

    cli = TinderCLI(tinder_token)
    requests.urllib3.disable_warnings()

    cmd = cli.get_cli_cmd(args.cmd)
    result = cli.run(cmd, tinder_id=args.id)

    print(result)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cmd', choices=TinderCLI.commands, default=False,
                        metavar='COMMAND', help=', '.join(TinderCLI.commands))
    parser.add_argument('--token', action='store', type=str, default=False,
                        metavar='TOKEN', help='tinder API token')
    parser.add_argument('--id', action='store', type=str, default=False,
                        metavar='TINDER ID', help='tinder profile ID')

    return parser.parse_args()


if __name__ == "__main__":
    main()
