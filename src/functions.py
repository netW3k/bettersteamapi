import traceback
import requests
import random


from difflib import get_close_matches as gcm


#TODO global values namespace, __main__ function do reaserch and procceed accordingly
_API1 = 'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
_API2 = 'https://store.steampowered.com/api/appdetails?appids='
_WISHEDCURRENCY = 'nok'


def __get_JSON(api, gameID = None):
     """
     This function requests steam API, converts it into a JSON and returns it
     
     :param api: Which API this function will request (_API1 OR _API2)
     :param gameID: gamID of the game you want to access details about, DEF:NONE
     :return: returns a JSON with 
     """
     
     # <IF SOMETHING GOES WRONG WITH THIS FUNCTION IT WILL RETURN 'NONETYPE' WHICH ESSENTIALY WILL MAKE EVERYTHING FALSE>

     try:
          if gameID == None: return requests.get(api).json()
          else: return requests.get(f"{api}{gameID}&cc={_WISHEDCURRENCY}").json()

     except Exception as e: 

               print('######################################################') #TODO CREATE BETTER EXCEPTION MENAGAMNET 
               print(f"\n ERROR OF PRIVATE FUNCTION - getJSON. RETRUNED AS : \n {traceback.format_exc()}. ABORT")
               print('######################################################') #TODO CREATE LOG FILE IF EXCEPTION RAISES 

               return None                        
               

def __is_success(id):
     # <This is function is needed in order to prevent any 'None-transcipable' errors, and mainly to check if Steam database consider the enry as successfull>
     
     try:
          game_JSON = __get_JSON(_API2, id)

          if game_JSON is None: return False

          return game_JSON[str(id)]['success'] 

     except Exception as e:

          print('######################################################')
          print(f"ERROR OF PRIVATE FUNCTION - isSuccess. ERROR AS : \n {traceback.format_exc()}. ABORT")
          print('######################################################')
          

def validate_game(game, return_gameID = False, suggestions = False,): #Returns a boolean value

     gameID = None
     game_suggestions = []

     game = game.lower()

     try:
          id_JSON = __get_JSON(_API1)

          if id_JSON is None: return 

          for item in id_JSON['applist']['apps']:
               
               if item['name'].lower() == game:

                    gameID = item['appid']

                    return gameID if return_gameID else __is_success(gameID) # <If the game exists and steam do have any record of the game, this should return True.>

               game_suggestions.append(item['name'])

          return gcm(game, game_suggestions, 10, 0.6) if suggestions is True else False # <Returns array of words that are similair to user input based on entries in id_JSON, if suggestions are set to true>
          
     except Exception as e:

          print("######################################################")
          print(f"ERROR OF PUBLIC FUNCTION validateGame! ERROR AS: \n {traceback.format_exc()}")
          print("######################################################")
          
          return None 


def game_description(gameID, option = 'short'):

     try:
          game_JSON = __get_JSON(_API2, gameID)
          
          if not __is_success(gameID): return None #WE NEED TO CHECK IF THE ENTRY IS CONSIDERED AS SUCCESSFULL IN STEAM API, IF NOT IT CAUSES ERROR

          if option == 'short': #TODO <IN PYTHON 3.10 YOU HAVE MATCH-CASE FUNCTION, HOWEVER IT'S NOT SUPPORTED WITH UBUNTU 20.04 (AS OF 16 MARCH 2022)> 
               
               description = game_JSON[str(gameID)]['data']['short_description']
              
               #long_desc = gamejs[str(appID)]['data']['detailed_description'] < RETURNED DATA IS WRITTEN IN SOME KIND OF MARKUP LANGUAGE AND IT'S IMPOSSIBLE AS OF NOW TO CLEAN THE OUTPUT, AND THERFORE IT'S COMMENTED OUT. MAYBE IT WILL BE IMPLEMENTED IN THE FUTURE RELEASE,BUT HIGHLY UNLIKELY>
              
               return description

     except Exception as e:

          print("################################################")
          print(f"ERROR OF PUBLIC FUNCTION gameDesc! ERROR AS: \n {traceback.format_exc()}")
          print("################################################")

          return None 


def release_date(gameID, comming_soon = False):

     game_JSON = __get_JSON(_API2, gameID)
     
     try:
          if comming_soon is True: return game_JSON[str(gameID)]['data']['release_date']['coming_soon'] 
          
          return game_JSON[str(gameID)]['data']['release_date']['date'] 

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - releaseDate. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None 


def is_free(gameID):

     game_JSON = __get_JSON(_API2,gameID)

     try: 
          return game_JSON[str(gameID)]['data']['is_free'] if game_JSON is not None else False
     
     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - isFree. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def store_page(gameID):

     try: 
          return f"https://store.steampowered.com/app/{str(gameID)}/?cc={_WISHEDCURRENCY}"
     
     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - storePage. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_price(appID):

     try: 
          if is_free(appID): return 'The game is free!'

          game_JSON = __get_JSON(_API2,appID)
          currency = game_JSON[str(appID)]['data']['price_overview']['currency']
          price = game_JSON[str(appID)]['data']['price_overview']['final_formatted']

          return f"{price} {currency}"

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePrice. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_discount(gameID, check_if_game_is_on_discount = False):

     try:
          if is_free(gameID) and check_if_game_is_on_discount == True: return False, 'FREE'
          elif is_free(gameID) and check_if_game_is_on_discount == False: return 'No discount, the game is free to play!'

          game_JSON = __get_JSON(_API2, gameID)
          discount = game_JSON[str(gameID)]['data']['price_overview']['discount_percent']
          
          return True if check_if_game_is_on_discount and discount > 0 else discount

     except Exception as e: 

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameDiscount. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def random_game(name_or_id = 'id'):

     try:
          id_JSON = __get_JSON(_API1)
          is_game = False
  
          while not is_game:
                    
               random_entry = random.choice(id_JSON['applist']['apps'])
               random_appID = str(random_entry['appid']) 
                                        
               try:
                    if not __is_success(random_appID): continue
                    
               except : continue

               game_JSON = __get_JSON(_API2, random_appID)

               if game_JSON[random_appID]['data']['type'] != 'game' : continue 
               
               is_game = True
          
          if name_or_id == 'name': return random_entry['name']
          elif name_or_id == 'both': return random_entry['name'], random_appID
          else: return random_appID
                              
     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - randomGame. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def random_free_game(name_or_id = 'id'):
     # <This function may take some time to proccess>
     #TODO Create possibilty to generate a JSON file of all free games with an update function

     try:
          id_JSON = __get_JSON(_API1)
          is_game = False

          while not is_game:

               random_entry = random.choice(id_JSON['applist']['apps'])
               random_appID = str(random_entry['appid'])

               try:
                    if not __is_success(random_appID): continue

               except: continue

               game_JSON = __get_JSON(_API2, random_appID)
               
               if not is_free(random_appID): continue
               if game_JSON[random_appID]['data']['type'] != 'game': continue

               is_game = True
          
          if name_or_id == 'name': return random_entry['name']
          elif name_or_id == 'both': return random_entry['name'], random_appID
          else: return random_appID

     except Exception as e: 

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - randomFreeGame. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_header_image(gameID):
     # <NOTE: This function returns a link to the image, this means that you need to proccess the return value and show it on your own>
     
     try: 
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)

          return game_JSON[str(gameID)]['data']['header_image']

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameHeaderImage. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_developers(gameID):
     # < Returns string as a connected elements of an array >

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)

          return ' , '.join(game_JSON[str(gameID)]['data']['developers'])

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameDev. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_publishers(gameID):
     # <  Returns string as a connected elements of an array >

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)

          return ' , '.join(game_JSON[str(gameID)]['data']['publishers'])

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePub. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_genres(gameID, return_array = False):

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)
          genres = []

          for item in game_JSON[str(gameID)]['data']['genres']:
          
               genres.append(item['description'])

          return genres if return_array is True else ' , '.join(genres)

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameGenre. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_categories(gameID, return_array = False):

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)
          categories = []

          for item in game_JSON[str(gameID)]['data']['categories']:

               categories.append(item['description'])

          return categories if return_array is True else ' , '.join(categories)

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameCat. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_platforms(gameID, return_dictionary = True):

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID) 
          platforms = {}
          game_on_platform = []
          
          for item in game_JSON[str(gameID)]['data']['platforms']:
          
               platforms[item] = game_JSON[str(gameID)]['data']['platforms'][item]     
          
          if return_dictionary is True: return platforms

          for item in platforms:

               if platforms[item] is True: game_on_platform.append(item)
                         
          return ' , '.join(game_on_platform)


     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePlatform. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


def game_support(gameID):

     try:
          if not __is_success(gameID) : return None

          game_JSON = __get_JSON(_API2, gameID)
          support_info = []

          for item in game_JSON[str(gameID)]['data']['support_info']:

               support_info.append(game_JSON[str(gameID)]['data']['support_info'][item])

          return support_info

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameSupport. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None


#game = 'scavengers'
#testID = validateGame(game, returnappID=True)
#if validateGame(game):
#     print(f"Test: {gameDesc(testID)}")
#else: print(f"Else test: {validateGame(game, suggestions=True)}")
#print(storePage(testID))
#print(gamePrice(testID))
#print(gameDiscount(testID))

#game = randomGame('id')
#print(gameSupport(game))
#print(f"{gameDev(game)} -- {gamePub(game)}")



