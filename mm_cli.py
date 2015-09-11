#! /usr/bin/env python3
# CLI interface for mgamcmahon program

import argparse
import sys
import os

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

    def addplayer(self):
        parser = argparse.ArgumentParser(
            description='Add a player. Name, rank, AGA ID, division')
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        parser.add_argument('player', nargs='*')
        #haven't figured out why nargs 3 or 5 doesn't work
        args = parser.parse_args(sys.argv[2:])

        h = open(args.filename, 'r')
        tournament = yaml.load(h.read())
        h.close()
        tournament.calculate_mm_score()
        if args.player:
            name = args.player[0]
            rank = int(args.player[1])
            aga_id = int(args.player[2])
            division = int(args.player[3])
            player = mcmahon.Player(name, rank, aga_id, [0, 0, 0], 0, division)
            tournament.add_player(player)
            h = open(args.filename, 'w')
            h.write(yaml.dump(tournament))
            h.close()
            print('Player {} successfully added'.format(player))

    def drop_player(self):
        parser = argparse.ArgumentParser(
            description='Drop a player by player ID')
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        parser.add_argument('player_id', nargs='*')
        args = parser.parse_args(sys.argv[2:])

        h = open(args.filename, 'r')
        tournament = yaml.load(h.read())
        h.close()
        tournament.calculate_mm_score()
        if args.player_id:
            player_id = int(args.player_id[0])
            tournament.drop_player(player_id)
            player = tournament.players[player_id]
            h = open(args.filename, 'w')
            h.write(yaml.dump(tournament))
            h.close()
            print('Player {}: {} successfully dropped'.format(player_id, player))

    def newtournament(self):
        parser = argparse.ArgumentParser(
            description='Generate new tournament')
        parser.add_argument('--handi', '-H',
                            action="store_true",
                            default=False,
                            help="Make tournament handicapped")
        parser.add_argument('--filename', '-f',
                            action="store",
                            default="tournament.yaml",
                            help="Default is 'tournament.yaml'")
        args = parser.parse_args(sys.argv[2:])

        if os.path.isfile(args.filename):
            raise RuntimeError('File {} already exists!'.format(args.filename))

        if args.handi:
            tournament = mcmahon.HandiTournament.new_tournament()
        else:
            tournament = mcmahon.Tournament.new_tournament()

        h = open(args.filename, 'w')
        h.write(yaml.dump(tournament))
        h.close()
        print('New tournament started and written to {}'.format(args.filename))

if __name__ == '__main__':
    MMCli()
