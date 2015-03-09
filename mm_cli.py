#! /usr/bin/env python3
# CLI interface for mgamcmahon program

import argparse
import mcmahon
import yaml

parser = argparse.ArgumentParser(description='CLI interface for mgamcmahon program')

parser.add_argument('--filename', '-f',
                    action="store",
                    default="tournament.yaml",
                    help="Filename of data. Default is 'tournament.yaml'")
parser.add_argument('--new-round', '-n',
                    action="store_true",
                    help="Generate new round")
parser.add_argument('--pairings_list', '-p',
                    action="store",
                    type=int,
                    help="Show pairings list for a round. 1 indexed")
parser.add_argument('--wall-list', '-w',
                    action="store_true",
                    help="Show current wall list")
parser.add_argument('--add-result', '-a',
                    action="store",
                    nargs=3,
                    help="Add a result. Round#, Board#, WinnerID#")

# Each time CLI is called, load the tournament, process command, then
# output to yaml and stdout.

args = parser.parse_args()
h = open(args.filename, 'r')
tournament = yaml.load(h.read())
h.close()
tournament.calculate_mm_score()

if args.new_round:
    tournament.start_new_round(tournament.generate_pairing(10000))
    print(tournament.rounds[-1]) # update with method for pairings
    print(yaml.dump(tournament))
    h = open(args.filename, 'w')
    h.write(yaml.dump(tournament))
    h.close()
    
if args.pairings_list:
    #args doesn't accept 0?
    print("Round {} pairing".format(args.pairings_list))
    print(tournament.rounds[args.pairings_list - 1])
    #update with method for pairings

if args.wall_list:
    print(tournament.wall_list())

if args.add_result:
    round_ = int(args.add_result[0]) - 1
    board = int(args.add_result[1])
    winner = int(args.add_result[2])
    tournament.add_result(round_, board, winner)
    h = open(args.filename, 'w')
    h.write(yaml.dump(tournament))
    h.close()

