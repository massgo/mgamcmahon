#! /usr/bin/env python3

# Mcmahon pairing for MGA tournament

import unittest

import yaml


class Player(object):

    def __init__(self, name, rank, aga_id, mm_score):
        self.name = name
        self.rank = rank
        self.aga_id = aga_id
        self.mm_score = mm_score

    def __repr__(self):
        return ('<{:s}(name={:s}, rank={:d}, aga_id={:d}, mm_score={:d})>'
                .format(self.__class__.__name__, self.name, self.rank, self.aga_id,
                        self.mm_score))

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return type(other) is not type(self) or self.__dict__ != other.__dict__


def player_representer(dumper, data):
    return dumper.represent_mapping('!player', data.__dict__)

yaml.add_representer(Player, player_representer)


def player_constructor(loader, node):
    player_dict = loader.construct_mapping(node)
    return Player(player_dict['name'], player_dict['rank'], player_dict['aga_id'],
                  player_dict['mm_score'])

yaml.add_constructor('!player', player_constructor)


class Tournament(object):

    def __init__(self, players, id_ctr):
        self.players = players
        self.id_ctr = id_ctr

    def standings(self):
        return sorted(list(self.players.keys()), key=lambda k: self.players[k].mm_score)

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return type(other) is not type(self) or self.__dict__ != other.__dict__


def tournament_representer(dumper, data):
    return dumper.represent_mapping('!tournament', data.__dict__)

yaml.add_representer(Tournament, tournament_representer)


def tournament_constructor(loader, node):
    tourn_dict = loader.construct_mapping(node)
    return Tournament(tourn_dict['players'], tourn_dict['id_ctr'])

yaml.add_constructor('!tournament', tournament_constructor)


class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        self.player_one = Player('Andrew', 10, 12345, 5000000)

    def test_repr(self):
        self.assertEqual(repr(self.player_one), '<Player(name=Andrew, rank=10,'
                                                ' aga_id=12345, mm_score=5000000)>')

    def test_yaml(self):
        self.assertEqual(self.player_one, yaml.load(yaml.dump(self.player_one)))


class TournamentTestCase(unittest.TestCase):

    def setUp(self):
        players = {0: Player('Andrew', 10, 12345, 5000000),
                   1: Player('Walther', 20, 1235, 10000)}
        self.tournament = Tournament(players, 2)

    def test_yaml(self):
        self.assertEqual(self.tournament, yaml.load(yaml.dump(self.tournament)))

if __name__ == '__main__':
    unittest.main()
