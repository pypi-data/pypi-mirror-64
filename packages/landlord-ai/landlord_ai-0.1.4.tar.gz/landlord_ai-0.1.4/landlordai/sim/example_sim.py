from landlordai.game.landlord import LandlordGame
from landlordai.game.player import LearningPlayer_v1, RandomPlayer
from landlordai.sim.simulate import Simulator

if __name__ == "__main__":
    players = [
        LearningPlayer_v1(name='3_29_v1', net_files=('../models/3_29_1_history.h5', '../models/3_29_1_position.h5'))
    ] * 2 + [LearningPlayer_v1(name='random')]

    simulator = Simulator(1, players)
    simulator.play_rounds()
    '''
    game = LandlordGame(players=players)
    game.play_round()
    for turn, move in game.get_move_logs():
        print(turn, move)
    '''
