#! /usr/bin/env python3

# Mcmahon pairing for MGA tournament

import random
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


class Pairing(object):

    def __init__(self, white, black, result=None):
        self.white = white
        self.black = black
        self.result = result


class Tournament(object):

    def __init__(self, players, id_ctr, rounds, old_pairs, current_players):
        self.players = players
        self.id_ctr = id_ctr
        self.rounds = rounds
        self.old_pairs = old_pairs
        self.current_players = current_players

    @classmethod
    def new_tournament(cls, players=None):
        tournament = cls({}, 0, [], set(), set())
        if players is not None:
            for player in players:
                tournament.add_player(player)
        return tournament

    def standings(self):
        return sorted(list(self.players.keys()), key=lambda k: self.players[k].mm_score)

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return type(other) is not type(self) or self.__dict__ != other.__dict__

    def add_player(self, player):
        self.players[self.id_ctr] = player
        self.id_ctr += 1

    def _round_is_valid(self, player_list):
        valid = True
        pairs = []
        temp_list = list(player_list)
        while player_list:
            pairs.append(frozenset([temp_list.pop(), temp_list.pop()]))
        for pair in pairs:
            if pair in self.old_pairs:
                valid = False
                break
        return valid
    
    def round_score(self, player_list):
        # measures sum of difference of mm_score per pairing
        # assumes even number of people?
        score = 0
        temp_list = list(player_list)
        while temp_list:
            score += abs(self.players[temp_list.pop()].mm_score -
                         self.players[temp_list.pop()].mm_score)
        return score

    def _generate_ideal_candidate_rounds(self, sample_size):
        mm_scores = set()
        for player in self.players:
            mm_scores.add(player.mm_score)

        while i < sample_size: 
            player_list = []
            for mm_score in mm_scores:
                player_sublist = [player_id for player_id, player in self.players.items()
                                  if player.mm_score == mm_score]
                random.shuffle(player_sublist)
                player_list.extend(player_sublist)
            yield player_list

    def _generate_candidate_rounds(self, sample_size):
        rounds = []
        for i in range(sample_size):
            player_list = []
            player_list.extend(self.players.keys())
            random.shuffle(player_list)
            rounds.append(player_list)
        return rounds

    def generate_round(self, sample_size): 
        # populate old pairs set, skip if first round
        if self.rounds:
            for pair in self.rounds[-1].values():
                self.old_pairs.add(frozenset([pair.black, pair.white]))
        #valid_rounds = [round_ for round_ in self._generate_candidate_rounds(sample_size)
        #                if self._round_is_valid(round_)]
        valid_rounds = self._generate_candidate_rounds(sample_size)
        best_score = 900000
        best_round = None
        for round_ in valid_rounds:
            round_score = self.round_score(round_)
            if round_score < best_score:
                best_score = round_score
                best_round = round_
        return best_round
        

def tournament_representer(dumper, data):
    return dumper.represent_mapping('!tournament', data.__dict__)

yaml.add_representer(Tournament, tournament_representer)


def tournament_constructor(loader, node):
    tourn_dict = loader.construct_mapping(node)
    return Tournament(tourn_dict['players'], tourn_dict['id_ctr'], tourn_dict['rounds'],
                      tourn_dict['old_pairs'], tourn_dict['current_players'])

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
        players = [Player('Ma Wang', 7, 12345, 6),
                   Player('Will', 4, 1235, 6),
                   Player('Steve', 4, 234, 6),
                   Player('Mr. Cho', 3, 54, 6),
                   Player('XiaoCheng', 3, 5723, 6),
                   Player('Alex', 1, 632, 6),
                   Player('Matt', 4, 5723, 6),
                   Player('Ed', 2, 5723, 6),
                   Player('Josh', 1, 5723, 6),
                   Player('Kevin', 1, 5723, 6),
                   Player('Gus', 1, 5723, 6),
                   Player('Pete', -2, 5723, 1),
                   Player('Dan', -1, 5723, 1),
                   Player('David', -2, 5723, 1),
                   Player('Alex', -3, 5723, 1),
                   Player('Eric', -4, 5723, 1),
                   Player('Makio', -4, 5723, 1),
                   Player('David', -4, 5723, 1),
                   Player('Eric', -4, 5723, 1),
                   Player('Howie', -4, 5723, 1),
                   ]
        self.tournament = Tournament.new_tournament(players)

    def test_yaml(self):
        self.assertEqual(self.tournament, yaml.load(yaml.dump(self.tournament)))

    def test_generate_round(self):
        round_ = self.tournament.generate_round(10000)
        self.assertEqual(self.tournament.round_score(round_), 5)


if __name__ == '__main__':
    unittest.main()
