import difflib
import random

import requests

import bettersteamapi.config as config


def change_wished_currency(currency: str) -> None:
     """ Change the wished currency you want the price to be in. Default value is USD (us)

          Some of the supported currencies:
               'us' - USD ($) American Dollars,

               'nok' - Norwegian Krones, 

               'au' - AUD (A$) Australian Dollars,

          If you change to a non-supported currency , steam will consider it as a default. 
          Meaning if you type "aud" instead of "au", the price will be shown with the 
          currency from the country your IP is registred in.

     Args:
          currency (str): The currency you want to change to.
     
     """ 
     config.wished_country_currency = currency
     #print(config.wished_country_currency)

         
def get_wished_currency() -> str:
     """ Get the the currency from the config file.

         If you want to change the current currency use 'change_wished_currency()' function

     Returns:
          String: The current currency that is set in config.json file
     """ 
     return config.wished_country_currency


def __get_json(gameid: str = 'None') -> dict:
     """This function requests steam API, converts it into a JSON and returns it

     Args:
          gameid (str): If empty this function will request API with all id's associated with a gamename,
                        if id is provided it will return dict with data associated with the id.

     Returns:
          Dictionary: If args is empty -> dict with ids and names of all games in steam DB.
                      If args not empty -> dict with all information about the specified game.
     """

     API1 = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
     API2 = "https://store.steampowered.com/api/appdetails?appids="

     if gameid == 'None': return requests.get(API1).json()

     return requests.get(f"{API2}{gameid}&cc={get_wished_currency()}").json()


def __is_success(gameid: str) -> bool:
     """Checks if the call is successful and if there is data avaiable.

     Args: 
          gameid(str): ID of the game

     Returns: 
          Boolean:  True -> the call is successful and listings are avaiable
                    False -> the call is unsuccessful, and something went wrong or there are no listing
                             for this ID.
     """
     # <This is function is needed in order to prevent any 'None-transcipable' errors, and mainly to check if Steam database consider the entry as successfull>

     game_json = __get_json(gameid)
     
     return game_json[gameid]["success"]


def validate_game(game_name: str, return_gameid: bool = False):
     """Validates if the game exists in DB, and has an option to return ID of specified game if 2nd arg is set to True.

     Args:
          game_name(str): name of the game you want to validate
          return_gameid(boolean): if you want to return ID of the game. (If game not found it will return 'None')

     Returns: 
          return_gameid: False -> returns bool based on if the game exist in steam DB or not
                         True -> returns ID of the game as string
     """
     
     game_name = game_name.lower()
     idjson = __get_json()

     for item in idjson["applist"]["apps"]:
        if item["name"].lower() == game_name and __is_success(str(item['appid'])):
            gameid = str(item["appid"]) 
            return gameid if return_gameid else True # <If the game exists and steam do have any record of the game, this should return True.>

     return False


def game_suggestions(game: str) -> list[str]:
     """ Get suggestions close to the specified game

     Args:
          game(str): name of the game you want to reference from 

     Returns: 
          List: returns a list(str)
     """

     game = game.lower()
     idjson = __get_json()
     gamelist = [item["name"] for item in idjson["applist"]["apps"]]

     return difflib.get_close_matches(word=game, possibilities=gamelist)


def get_game_description(gameid: str) -> str:
     ''' Get short description of the game
     '''
     gamejson = __get_json(gameid)
     return gamejson[gameid]["data"]["short_description"]


def get_release_date(gameid: str, return_comming_soon: bool = False) -> str:
     """Get the release date of the provided game. Optional: return bool based on if the game is comming soon or not.
     
     Args:
          gameid(str): ID of the game
          return_comming_soon(bool): if set to True, checks and returns if a game is officialy released 
                               or is releasing soon on platform.
     
     Returns:
          return_comming_soon: True -> returns bool based on if the game is comming soon.
                               False -> returns the release date of the game
     """

     gamejson = __get_json(gameid)
     coming_soon = gamejson[str(gameid)]["data"]["release_date"]["coming_soon"]

     if return_comming_soon is True: return coming_soon
     return gamejson[str(gameid)]["data"]["release_date"]["date"]


def check_if_free(gameid: str) -> bool:
     game_json = __get_json(gameid)

     return (game_json[str(gameid)]["data"]["is_free"] if game_json is not None else False)


def get_store_page(gameid: str) -> str:
     ''' Get the steam store pageof the game

     Returns a link to the storepage.
     '''
     return f"https://store.steampowered.com/app/{gameid}/?cc={get_wished_currency()}"


def get_game_price(gameid: str) -> str:
    
     if check_if_free(gameid): return "The game is free!"

     gamejson = __get_json(gameid)
     
     try:
          currency = gamejson[str(gameid)]["data"]["price_overview"]["currency"]
          price = gamejson[str(gameid)]["data"]["price_overview"]["final_formatted"]

     except KeyError:
          print('Could not find the specified key in JSON file.')
          return 'None'

     return f"{price} {currency}"


def get_game_discount(gameid: str,) -> str:
     """ Get the discount of the game.

     Returns:
          String -> Returns the discount value in percent. 
     """
     gamejson = __get_json(gameid)
     discount = str(gamejson[str(gameid)]["data"]["price_overview"]["discount_percent"])

     return discount


def check_if_game_on_discount(gameid: str) -> bool:
     """ Check if the provided game is on discount.

     Raises:
          KeyError: One of the keys are not present in the JSON file of the provided game. 
                    Is raised when JSON key is missing. If the game is free to play it can cause 
                    this error to raise. 
     
     Returns:
          Boolean: True if the game is on discount (not 0), False if the game is not on discount (0)
     """
     if check_if_free(gameid): return False

     gamejson = __get_json(gameid)

     try:
          discount = gamejson[str(gameid)]["data"]["price_overview"]["discount_percent"]

     except KeyError: 
          print('The price value key is not listed in JSON file. Check if provided game is not free-to-play')
          return False

     return True if discount > 0 else False


def get_random_game() -> dict[str, str]:
     """Get random game from steam applist, checks if it is a game and returns dict with name and id.
        
        Keys: 'name' | 'appid'
     """
    
     idjson = __get_json()
     is_game = False
     random_game = {}

     while not is_game:
          random_entry = random.choice(idjson['applist']['apps'])
          random_appid = str(random_entry['appid'])

          if not __is_success(random_appid): continue 

          gamejson = __get_json(random_appid)
          
          if gamejson[random_appid]['data']['type'] != 'game': continue

          is_game = True
          random_game = {"name" : random_entry['name'], "appid" : str(random_entry['appid'])} # needed in order to change id from integer to a string data type
          
     
     return random_game
     

def random_free_game() -> dict[str, str]:
     """Get random free game from steam applist, checks if it is a game and returns dict with name and id.
        
        NOTE -> This function can take some time before returning a value.
        
        Keys: 'name' | 'appid'
     """

     # TODO Create possibilty to generate a JSON file of all free games with an update function. Create a new module 
     # for this?

     # <This function may take some time to proccess and return a value>

     idjson = __get_json()
     is_game = False
     random_game = {}

     while not is_game:

          random_entry = random.choice(idjson['applist']['apps'])
          random_appid = str(random_entry['appid'])

          if not __is_success(random_appid): continue

          game_JSON = __get_json(random_appid)

          if not check_if_free(random_appid): continue
          if game_JSON[random_appid]['data']['type'] != 'game': continue

          is_game = True
          random_game = {"name" : random_entry['name'], "appid" : str(random_entry['appid'])}
          # needed in order to change id from integer to a string data type

     return random_game


def game_header_image(gameid: str) -> str:
     """Get the header image of the game.
     
     Returns: 
          String -> link to the header image. Useful if frontend automatically gets the image by providing link to the 
                    image.
     """

     gamejson = __get_json(gameid)

     return gamejson[gameid]['data']['header_image']


def game_developers(gameID: str) -> list[str]:
     """Get a list of game developers.

     Raises:
          KeyError: One of the keys are not present in the JSON file of the provided game.
                    KeyError returns empty list.
     """

     game_JSON = __get_json(gameID)

     try:     
          return game_JSON[gameID]['data']['developers']

     except KeyError:
          print("Could not find the 'developers' key in the JSON file/request.")
          return []

def game_publishers(gameid: str) -> list[str]:
     """Get a list of game publishers.

     Raises:
          KeyError: One of the keys are not present in the JSON file of the provided game.
                    KeyError returns empty list.
     """

     gamejson = __get_json(gameid)
     
     try:
          return gamejson[gameid]['data']['publishers']

     except KeyError:
          print("Could not find the 'publishers' key in the JSON file/request")
          return []

def game_genres(gameid: str) -> list[str]:
     """Get a list of game generes.
     """

     gamejson = __get_json(gameid)
     genres = []

     for item in gamejson[gameid]['data']['genres']:
          genres.append(item['description'])

     return genres


def game_categories(gameid: str) -> list[str]:
     """Get a list of all categories the game is listed as. 
     """

     gamejson = __get_json(gameid)
     categories = []

     for item in gamejson[str(gameid)]['data']['categories']:
          categories.append(item['description'])

     return categories 


def game_platforms(gameid: str) -> dict[str, bool]:
     """Get dict of platforms.

     Returns: Dictionary with all steam supported platforms and bool value 
     on whether the game is avaiable on named platform or not.
     
     Keys: 'windows' | 'mac' | 'linux'
     """

     gamejson = __get_json(gameid)
     platforms = {}

     for item in gamejson[gameid]['data']['platforms']:
          platforms[item] = gamejson[gameid]['data']['platforms'][item]

     return platforms


def game_support(gameid: str) -> dict[str, str]:
     """Get dict with support details of the game. 
     
        Keys: 'url' | 'email'
     """

     gamejson = __get_json(gameid)

     return gamejson[gameid]['data']['support_info']
