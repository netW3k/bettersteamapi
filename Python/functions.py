import traceback
import requests
import random

from difflib import get_close_matches as gcm

#TODO Check if you need __isSuccess in every method or not
__API1 = 'https://api.steampowered.com/ISteamApps/GetAppList/v0002/?key=STEAMKEY&format=json'
__API2 = 'https://store.steampowered.com/api/appdetails?appids='
__WISHEDCURRENCY = 'nok'


def __getJSON(api, appid = None):
     # <IF SOMETHING GOES WRONG WITH THIS FUNCTION IT WILL RETURN 'NONETYPE' WHICH ESSENTIALY WILL MAKE EVERYTHING FALSE>
     ## DEV NOTE ## Be careful of arguments/parameters placement. API is FIRST declared, and appid second. 


     try:
          if appid == None: return requests.get(api).json()
          else: return requests.get(f"{api}{appid}&cc={__WISHEDCURRENCY}").json()



     except Exception as e: 

               print('######################################################') #TODO CREATE BETTER EXCEPTION MENAGAMNET 
               print(f"\n ERROR OF PRIVATE FUNCTION - getJSON. RETRUNED AS 'NONE' \n {e} ")
               print('######################################################')
               #print(e)
               #traceback.format_exc() #TODO CREATE LOG FILE IF EXCEPTION RAISES 
               return None                        
               

def __isSuccess(gameID):
     # <This is function is needed in order to prevent any 'None-transcipable' errors, and mainly to check if Steam database consider the enry as successfull>
     
     tempjs = __getJSON(__API2, gameID)

     if tempjs is None: return False

     try:
          return tempjs[str(gameID)]['success'] 

     except Exception as e:

          print('######################################################')
          print(f"ERROR OF PRIVATE FUNCTION - isSuccess. ERROR AS : ")
          print('######################################################')
          traceback.format_exc()


def validateGame(game, returnappID = False, suggestions = False,): #Returns a boolean value

     appID = None
     gamesuggestions = []

     game = game.lower()

     #print("Validatating " + game)

     try:
          appjs = __getJSON(__API1)
          if appjs is None: return 

          for item in appjs['applist']['apps']:
               
               if item['name'].lower() == game:

                    appID = item['appid']

                    #print(appID)

                    return appID if returnappID else __isSuccess(appID) # < If the game exists and steam do have any record of the game, this should return True.  >

               gamesuggestions.append(item['name'])

          if not suggestions:
               return False

          return gcm(game, gamesuggestions, 10, 0.6)
          
     
     except Exception as e:

          print("######################################################")
          print(f"ERROR OF PUBLIC FUNCTION validateGame! ERROR AS: ")
          print("######################################################")
          traceback.format_exc()
          
          
          return None 


def gameDesc(appID, option = 'short'):

     try:
          gamejs = __getJSON(__API2, appID)
          
          if not __isSuccess(appID): #WE NEED TO CHECK IF THE ENTRY IS CONSIDERED AS SUCCESSFULL IN STEAM API, IF NOT IT CAUSES ERROR
               return None 

          if option == 'short': #TODO <IN PYTHON 3.10 YOU HAVE MATCH-CASE FUNCTION, HOWEVER IT'S NOT SUPPORTED WITH UBUNTU 20.04 (AS OF 16 MARCH 2022)> 
               
               desc = gamejs[str(appID)]['data']['short_description']
              
               #long_desc = gamejs[str(appID)]['data']['detailed_description'] < RETURNED DATA IS WRITTEN IN SOME KIND OF MARKUP LANGUAGE AND IT'S IMPOSSIBLE AS OF NOW TO CLEAN THE OUTPUT, AND THERFORE IT'S COMMENTED OUT. MAYBE IT WILL BE IMPLEMENTED IN THE FUTURE RELEASE,BUT HIGHLY UNLIKELY>
              
               return desc

     except Exception as e:

          print("###############################################")
          print(f"ERROR OF PUBLIC FUNCTION gameDesc! ERROR AS: ")
          print("###############################################")
          traceback.format_exc()

          return None 


def releaseDate(gameID, csoon = False):

     gamejs = __getJSON(__API2, gameID)
     
     try:
          if csoon: return gamejs[str(gameID)]['data']['release_date']['coming_soon'] 
          
          return gamejs[str(gameID)]['data']['release_date']['date'] 

     except Exception as e:

               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - releaseDate. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')

               return None 


def isFree(gameID):

     gamejs = __getJSON(__API2,gameID)

     try: 
          return gamejs[str(gameID)]['data']['is_free'] if gamejs is not None else False
     
     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - isFree. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def storePage(gameID):

     try: return f"https://store.steampowered.com/app/{str(gameID)}/?cc={__WISHEDCURRENCY}"
     
     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - storePage. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gamePrice(appID):

     try: 

          if isFree(appID): return 'The game is free!'

          gamejs = __getJSON(__API2,appID)
          currency = gamejs[str(appID)]['data']['price_overview']['currency']
          price = gamejs[str(appID)]['data']['price_overview']['final_formatted']

          return f"{price} {currency}"

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePrice. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameDiscount(gameID, checkifgameisondiscount = False):

     try:

          if isFree(gameID) and checkifgameisondiscount == True: return False, 'FREE'
          elif isFree(gameID) and checkifgameisondiscount == False: return 'No discount, the game is free to play!'

          gamejs = __getJSON(__API2, gameID)
          discount = gamejs[str(gameID)]['data']['price_overview']['discount_percent']
          
          return True if checkifgameisondiscount and discount > 0 else discount

     except Exception as e: 
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameDiscount. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def randomGame(nameorid = 'id'):

     try:
          appjs = __getJSON(__API1)
          isgame = False
  
          while not isgame:
                    
               random_entry = random.choice(appjs['applist']['apps'])
               random_appID = str(random_entry['appid']) 
                                        
               try:
                    
                    if not __isSuccess(random_appID): continue
                    
               except : continue

               gamejs = __getJSON(__API2, random_appID)

               if gamejs[random_appID]['data']['type'] != 'game' : continue 
               
               isgame = True
          
          if nameorid == 'name': return random_entry['name']
          elif nameorid == 'both': return random_entry['name'], random_appID
          else: return random_appID
          
                         
     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - randomGame. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def randomFreeGame(nameorid = 'id'):
     # <This function may take some time to proccess>
     #TODO Create possibilty to generate a JSON file of all free games with an update function
     try:
          appjs = __getJSON(__API1)
          isgame = False

          while not isgame:

               random_entry = random.choice(appjs['applist']['apps'])
               random_appID = str(random_entry['appid'])

               try:

                    if not __isSuccess(random_appID): continue

               except: continue

               gamejs = __getJSON(__API2, random_appID)
               
               if not isFree(random_appID): continue
               if gamejs[random_appID]['data']['type'] != 'game': continue

               isgame = True
          
          if nameorid == 'name': return random_entry['name']
          elif nameorid == 'both': return random_entry['name'], random_appID
          else: return random_appID

     except Exception as e: 
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - randomFreeGame. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameHeaderImage(gameID):
     # <NOTE: This function returns a link to the image, this means that you need to proccess the return value and show it on your own>
     try: 
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)

          return gamejs[str(gameID)]['data']['header_image']

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameHeaderImage. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameDev(gameID):
     # < Returns string as a connected elements of an array >

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)

          return ' , '.join(gamejs[str(gameID)]['data']['developers'])

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameDev. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gamePub(gameID):
     # <  Returns string as a connected elements of an array >

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)

          return ' , '.join(gamejs[str(gameID)]['data']['publishers'])

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePub. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameGenre(gameID, arrayasoutput = False):

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)
          genres = []

          for item in gamejs[str(gameID)]['data']['genres']:
          
               genres.append(item['description'])

          return genres if arrayasoutput is True else ' , '.join(genres)

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameGenre. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameCat(gameID, arrayisoutput = False):

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)
          cat = []

          for item in gamejs[str(gameID)]['data']['categories']:

               cat.append(item['description'])

          return cat if arrayisoutput is True else ' , '.join(cat)

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gameCat. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gamePlatform(gameID, dctasoutput = True):

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID) 
          platforms = {}
          onplatform = []
          
          for item in gamejs[str(gameID)]['data']['platforms']:
          
               platforms[item] = gamejs[str(gameID)]['data']['platforms'][item]     
          
          if not dctasoutput:
               for item in platforms:
                    if platforms[item] is True:
                         onplatform.append(item)
                    
               return ' , '.join(onplatform)

          return platforms

     except Exception as e:
               print('######################################################')
               print(f"ERROR OF PUBLIC FUNCTION - gamePlatform. ERROR AS : \n {traceback.format_exc()}")
               print('######################################################')
               return None


def gameSupport(gameID):

     try:
          if not __isSuccess(gameID) : return None

          gamejs = __getJSON(__API2, gameID)
          supportinfo = []

          for item in gamejs[str(gameID)]['data']['support_info']:
               supportinfo.append(gamejs[str(gameID)]['data']['support_info'][item])

          return supportinfo

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



