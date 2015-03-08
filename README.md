-- bands will be manually assigned in the yaml file at the beginning of the tournament as part of player registration/checkin.

round is {}
rounds is []

class Tournament

self.players = {player_id: Player}
self.id_ctr = Int
self.rounds = []
self.old_pairs = set()
self.current_players = set()

round or player_list is list of player ids

