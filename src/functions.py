import json
import random
from difflib import get_close_matches as gcm

import requests


def __get_json(gameid: str = 'None') -> dict:
    """This function requests steam API, converts it into a JSON and returns it

    :param gameid: If empty this function will request API with all id's associated with a gamename
    :returns: JSON with all id's with gamenames existing in steam DB or JSON with details about a game (if gameID has a valid ID of the game)
    """
    # <IF SOMETHING GOES WRONG WITH THIS FUNCTION IT WILL RETURN 'NONE' WHICH ESSENTIALY WILL MAKE EVERYTHING FALSE>

    API1 = "https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json"
    API2 = "https://store.steampowered.com/api/appdetails?appids="

    configjson = json.load(open(file="./config.json", encoding="utf-8"))

    if gameid == 'None': return requests.get(API1).json()

    return requests.get(f"{API2}{gameid}&cc={configjson['wished_country_currency']}").json()


def __is_success(id: str) -> bool:
    """
    Returns whatever value is under JSON 'success' key, if None it returns False. Used to check if a game is recognized as successfull in steam DB.
    This function is mainly used to check if a game is True under 'success', if not, it means that something is wrong, and therfore it is used as a
    prevention function (if returns False, evereything else will return False or None).
    """
    # <This is function is needed in order to prevent any 'None-transcipable' errors, and mainly to check if Steam database consider the enry as successfull>

    game_json = __get_json(id)

    return game_json[id]["success"]


def validate_game(game: str, return_gameid: bool = False) -> bool:
     """Validates if provided game exists in steam DB.

     :param game: Name of the game to validate.
     :param return_gameid: If this function should return ID of the game (if not found, return None)
     :return: returns a boolean value based on if the game was found or not, if return_gameID is set to False, otherwise it will return gameID
     """
     
     game = game.lower()
     idjson = __get_json()

     for item in idjson["applist"]["apps"]:
        if item["name"].lower() == game:
            gameid = item["appid"]
            return (gameid if return_gameid else True)  # <If the game exists and steam do have any record of the game, this should return True.>

     return False

def game_suggestions(game: str) -> list[str]:
     """ Returns suggestions based on game value.
     :param game: name of the game you want to get suggestions 
     :returns: list of strings that are similair to game value
     """

     game = game.lower()
     idjson = __get_json()
     gamelist = [item["name"] for item in idjson["applist"]["apps"]]

     return gcm(word=game, possibilities=gamelist)


def get_game_description(gameid: str) -> str:
     gamejson = __get_json(gameid)
     return gamejson[gameid]["data"]["short_description"]


def get_release_date(gameid: str, return_comming_soon: bool = False) -> str:
     """Get the release date of the provided game.

     :param return_coming__soon: if True, it checks and returns if a game officialy released or is releasing soon on platform as bool.
     """

     gamejson = __get_json(gameid)
     coming_soon = gamejson[str(gameid)]["data"]["release_date"]["coming_soon"]

     if return_comming_soon is True: return coming_soon
     return gamejson[str(gameid)]["data"]["release_date"]["date"]


def check_if_free(gameid: str) -> bool:
     """ Checks if a game is free.
     """

     game_json = __get_json(gameid)
     return (game_json[str(gameid)]["data"]["is_free"] if game_json is not None else False)


def get_store_page(gameid: int) -> str:
     configjson = json.load(open(file="./config.json", encoding="utf-8"))
     return f"https://store.steampowered.com/app/{str(gameid)}/?cc={configjson['wished_country_currency']}"


def get_game_price(appid: str) -> str:
     """Get price of the game. (This function sometimes returns other currencies than expected. This most likely has to do with servers and which one you request from)

     :returns: String with price and name of the currency. This is the final price, which means that if a game is on discount, this price will change accordingly.
     """
    
     if check_if_free(appid): return "The game is free!"

     gamejson = __get_json(appid)
     currency = gamejson[str(appid)]["data"]["price_overview"]["currency"]
     price = gamejson[str(appid)]["data"]["price_overview"]["final_formatted"]

     return f"{price} {currency}"


def get_game_discount(gameid: str, check_if_game_is_on_discount: bool = False):
     """Get the discount of the game.

     :check_if_game_is_on_discount: If set to True, this function will return True if the provided game is on discount.
     :returns: Integer
     """
    
     if check_if_free(gameid) and check_if_game_is_on_discount == True: return False, "FREE"
     elif check_if_free(gameid) and check_if_game_is_on_discount == False: return "No discount, the game is free to play!"
     
     gamejson = __get_json(gameid)
     discount = gamejson[str(gameid)]["data"]["price_overview"]["discount_percent"]

     return True if check_if_game_is_on_discount and discount > 0 else discount


def get_random_game() -> dict[str, str]:
     """Random game from steam applist, checks if it is a game and returns based on parameter.
        
        :returns: a dictionary with a 'name' and a 'appid' of the game
     """
    
     idjson = __get_json()
     is_game = False

     while not is_game:
          random_entry = random.choice(idjson["applist"]["apps"])
          random_appid = str(random_entry["appid"])
          if not __is_success(random_appid): continue #TODO what if this is in get json method

          gamejson = __get_json(random_appid)
          
          if gamejson[random_appid]["data"]["type"] != "game": continue

          is_game = True
          random_game = {"name" : random_entry['name'], "appid" : str(random_entry['appid'])}
     
     return random_game
     

def random_free_game() -> dict:
     """Random free game from steam applist, checks if it is a game and returns based on parameter.
        
        :returns: a dictionary with a 'name' and 'appid' of the game.
     """

     # <This function may take some time to proccess>
     # TODO Create possibilty to generate a JSON file of all free games with an update function


     idjson = __get_json()
     is_game = False

     while not is_game:

          random_entry = random.choice(idjson["applist"]["apps"])
          random_appid = str(random_entry["appid"])

          if not __is_success(random_appid): continue

          game_JSON = __get_json(random_appid)

          if not check_if_free(random_appid): continue
          if game_JSON[str(random_appid)]["data"]["type"] != "game": continue

          is_game = True

     return random_entry



def game_header_image(gameid: str) -> str:
     """Get the header image of the game.
     :returns: Link as a string to the image.
     """
     # <NOTE: This function returns a link to the image, this means that you need to proccess the return value and show it on your own>

     gamejson = __get_json(gameid)

     return gamejson[gameid]["data"]["header_image"]


def game_developers(gameID: str) -> list:
     """Get a list of game developers..
     """

     game_JSON = __get_json(gameID)
     
     return game_JSON[gameID]["data"]["developers"]


def game_publishers(gameid: str) -> list:
     """Get a list of game publishers.
     """

     gamejson = __get_json(gameid)

     return gamejson[gameid]["data"]["publishers"]


def game_genres(gameid: str) -> list:
     """Get a list of game generes.
     """

     gamejson = __get_json(gameid)
     genres = []

     for item in gamejson[gameid]["data"]["genres"]:
          genres.append(item["description"])

     return genres


def game_categories(gameid: str) -> list:
     """Get a list of game categories.

     """

     gamejson = __get_json(gameid)
     categories = []

     for item in gamejson[str(gameid)]["data"]["categories"]:
          categories.append(item["description"])

     return categories 



def game_platforms(gameid: str) -> dict:
     """Get's a dictionary of platforms and returns all platforms the game is avaiable on.
     :returns: All platform names, the provided game is avaiable on as a string.
     """

     gamejson = __get_json(gameid)
     platforms = {}

     for item in gamejson[gameid]["data"]["platforms"]:
          platforms[item] = gamejson[gameid]["data"]["platforms"][item]

     return platforms


def game_support(gameid: str) -> list:
     """Get list with support details.
     """

     gamejson = __get_json(gameid)
     support_info = []

     for item in gamejson[gameid]["data"]["support_info"]:
          support_info.append(gamejson[gameid]["data"]["support_info"][item])

     return gamejson[gameid]["data"]["support_info"]



# game = 'scavengers'
# testID = validateGame(game, returnappID=True)
# if validateGame(game):
#     print(f"Test: {gameDesc(testID)}")
# else: print(f"Else test: {validateGame(game, suggestions=True)}")
# print(storePage(testID))
# print(gamePrice(testID))
# print(gameDiscount(testID))

# game = randomGame('id')
# print(gameSupport(game))
# print(f"{gameDev(game)} -- {gamePub(game)}")
