#! /usr/bin/env python3
# CLI interface for mgamcmahon program

import argparse
import sys

import yaml

import mcmahon


class MMCli(object):

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='CLI interface for mgamcmahon program',
            usage='''mmcli <command> [<args>]

            Command options:

            newround
            show <[pairings], [standings]>
            add-result <round#, board#, winner#>''')

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        # simple way to get command names, but does not allow
        # dashes in name
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # tournament is not loaded until all args and subargs parsed
        getattr(self, args.command)()

    def newround(self):
        parser = argparse.ArgumentParser(
            description='Generate new round')
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        args = parser.parse_args(sys.argv[2:])

        h = open(args.filename, 'r')
        tournament = yaml.load(h.read())
        h.close()

        tournament.calculate_mm_score()
        tournament.start_new_round(tournament.generate_pairing(10000))
        #print(tournament.rounds[-1])  # update with method for pairings
        print(yaml.dump(tournament))
        h = open(args.filename, 'w')
        h.write(yaml.dump(tournament))
        h.close()

    def show(self):
        parser = argparse.ArgumentParser(
            description='Print out pairings or standings')
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        parser.add_argument('output',
                            choices=['pairings', 'standings'])
        args = parser.parse_args(sys.argv[2:])

        h = open(args.filename, 'r')
        tournament = yaml.load(h.read())
        h.close()
        tournament.calculate_mm_score()

        if args.output == 'pairings':
#            for round_ in tournament.rounds:
#                print(round_)
            print(tournament.pairings_list())
        else:
            print(tournament.wall_list())

    def addresult(self):
        parser = argparse.ArgumentParser(
            description='Add a result. Round#, Board#, Winner#')
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        parser.add_argument('result', nargs='*')
        #haven't figured out why nargs 3 or 5 doesn't work
        args = parser.parse_args(sys.argv[2:])
        print(args)

        h = open(args.filename, 'r')
        tournament = yaml.load(h.read())
        h.close()
        tournament.calculate_mm_score()
        if args.result:
            round_ = int(args.result[0]) - 1
            board = int(args.result[1])
            winner = int(args.result[2])
            tournament.add_result(round_, board, winner)
            h = open(args.filename, 'w')
            h.write(yaml.dump(tournament))
            h.close()

if __name__ == '__main__':
    MMCli()

