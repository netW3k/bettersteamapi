import functions

game = functions.get_random_game()
print(game['appid'])
print(functions.game_support(game['appid']))
print(game['name'])
