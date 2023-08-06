
import random

import numpy as np
from scipy import sparse

from landlordai.game.landlord import LandlordGame
from landlordai.game.player import TurnPosition


class Simulator:
    def __init__(self, rounds, player_pool):
        self.rounds = rounds
        self.player_pool = player_pool
        self.sparse_record_states = []
        self.move_vectors = []
        self.q = []
        self.win_matrix = np.zeros((len(player_pool), len(player_pool)))
        self.player_map = dict([(player, i) for (i, player) in enumerate(self.player_pool)])

    def play_rounds(self, debug=False):
        for r in range(self.rounds):
            if debug:
                print('Playing Round ', r)
            self.play_game()
        if debug:
            print('Done Playing')

    def play_game(self):
        while True:
            players = self.pick_players()
            game = LandlordGame(players=players)
            # play a meaningful game
            game.play_round()
            if game.has_winners():
                for pos in game.winners:
                    player = game.get_ai(pos)
                    self.sparse_record_states.extend([sparse.csr_matrix(x) for x in player.get_record_history_matrices()])
                    self.move_vectors.extend(player.get_record_move_vectors())
                    self.q.append(player.get_future_q())
                    player.reset_records()
                self.track_stats(game, players)
                break

            # clear out in case a full game wasn't played
            for player in players:
                player.reset_records()

    def track_stats(self, game: LandlordGame, players):
        winners = []
        losers = []
        for pos in list(TurnPosition):
            if pos in game.get_winners():
                winners.append(players[pos])
            else:
                losers.append(players[pos])

        for winner in winners:
            for loser in losers:
                self.win_matrix[self.player_map[winner], self.player_map[loser]] += 1

    def get_win_rate(self, player):
        player_index = self.player_map[player]
        wins = np.sum(self.win_matrix[player_index])
        losses = np.sum(self.win_matrix[: player_index])
        self_plays = np.sum(self.win_matrix[player_index, player_index])

        total_games = wins + losses - self_plays * 2
        return wins / total_games

    def pick_players(self):
        return random.sample(self.player_pool, LandlordGame.NUM_PLAYERS)

    def get_sparse_game_data(self):
        return self.sparse_record_states, np.vstack(self.move_vectors), np.hstack(self.q)
