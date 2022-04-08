import functions

game = functions.get_random_game()
print(game['appid'])
print(functions.game_categories(game['appid']))
print(game['name'])
print(functions.game_support(game['appid']))
