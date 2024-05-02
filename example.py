from pypokerengine.api.game import setup_config, start_poker
from randomplayer import RandomPlayer
from raise_player import RaisedPlayer
from testPlayerLeVi import TestPlayer

#TODO:config the config as our wish
config = setup_config(max_round=20, initial_stack=10000, small_blind_amount=10)



config.register_player(name="f1", algorithm=TestPlayer())
config.register_player(name="FT2", algorithm=RaisedPlayer())

game_result = start_poker(config, verbose=1)

# win_count = 0
# for i in range(0, 100):
#     game_result = start_poker(config, verbose=1)
#     stack = game_result['players'][0]['stack']
#     if stack > 10000:
#         win_count += 1
#     elif stack == 10000:
#         win_count += 0.5

# print('Win rate is: ' + str(win_count / 100))
