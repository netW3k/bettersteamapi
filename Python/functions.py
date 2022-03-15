import requests
from difflib import get_close_matches as gcm







def validate_game(game, suggestions = False,): #Returns a boolean value

     appID = None
     gamesuggestions = []
     game = game.lower()

     print("Validatating " + game)

     try:
          appjs = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json').json()

          for item in appjs['applist']['apps']:
               
               if item['name'].lower() == game:

                    appID = item['appid']

                    gamejs = requests.get(f'https://store.steampowered.com/api/appdetails?appids={appID}').json()
                    print(appID)

                    return gamejs[str(appID)]['success'] #If the game exists and steam do have any record of the game, this should return True 

               gamesuggestions.append(item['name'])

          if not suggestions:
               return False

          return gcm(game, gamesuggestions, 10, 0.6)
          

     except Exception as e:
          print("#########################################################################################")
          print(f"Error of validating! Error as: {e}")
          print("#########################################################################################")
          return None #None or null? #TODO 



