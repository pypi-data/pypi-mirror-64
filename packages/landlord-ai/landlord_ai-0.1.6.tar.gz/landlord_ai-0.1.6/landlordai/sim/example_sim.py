from landlordai.game.landlord import LandlordGame
from landlordai.game.player import LearningPlayer_v1, RandomPlayer
from landlordai.sim.game_stats import GameStats
from landlordai.sim.simulate import Simulator

if __name__ == "__main__":
    players = [
        LearningPlayer_v1(name='3_29_v1', net_dir='../models/3_29_1')
    for _ in range(3)] + [LearningPlayer_v1(name='random') for _ in range(3)]

    simulator = Simulator(20, players)
    simulator.play_rounds()
    results = simulator.get_result_pairs()

    stats = GameStats(players, results)

    print(stats.get_win_rate('random'))
    print(stats.get_win_rate('3_29_v1'))

    #game = LandlordGame(players=players)
    #game.play_round()
    #for turn, move in game.get_move_logs():
    #    print(turn, move)

