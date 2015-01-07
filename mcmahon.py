#! /usr/bin/env python3

# Mcmahon pairing for MGA tournament

import yaml

class Player(object):
    
    def from_dict(player_dict):
        player = Player()
        player.name = player_dict['name'] 
        player.rank = player_dict['rank']
        player.aga_id = player_dict['aga_id']
        return player

    def __repr__(self):
        return '<{:s}(name={:s}, rank={:d}, aga_id={:d})>'.format(self.__class__.__name__, self.name, self.rank, self.aga_id)

class Tournament(object):

    def from_yaml (yaml_file):
        tournament = Tournament()
        tourn_dict = yaml.load(yaml_file) 
        tournament.players = set()
        for player_dict in tourn_dict['players']:
            tournament.players |= {Player.from_dict(player_dict)}
        return tournament

if __name__ == '__main__':
    test = Tournament.from_yaml(open("tournament.yaml", 'r+'))
    print(test.players)

