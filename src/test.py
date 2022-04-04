import functions as BAS

usermode = ''

GAME_INFO = '1'
RANDOM_GAME = '2'
FREE_RANDOM_GAME = '3'
EXIT = '4'


while usermode != EXIT:

     validInput = False

     print('\n#######################################')
     print('<-- BetterSteamApi -- BAS -- Showcase -->')
     print('#######################################\n')
     print('1. Game Information')
     print('2. Give me a random game')
     print('3. Give me a random FREE game')
     print('4. Exit')

     while validInput is False:
          
          usermode = input('What would you like to do? ')

          if usermode == GAME_INFO or usermode == RANDOM_GAME or usermode == FREE_RANDOM_GAME or usermode == EXIT: 
               validInput = True # <Not ideal way of checking user input, however it serves its purpose>
     
     if usermode == EXIT : break

     if usermode == GAME_INFO : 
          
          exists = False
          iteration = 0
          while exists is False:

               iteration += 1

               if iteration != 1: print(BAS.validate_game(gamename, suggestions = True))
               gamename = ''
               gamename = input('What is the name of the game? ')
               
               #print(f"Try: {gamename}")
               #print(BAS.validate_game(gamename))

               if BAS.validate_game(gamename) is False: continue
                   
               gameID = BAS.validate_game(gamename, True)
               exists = True

     elif usermode == RANDOM_GAME : 
          gamename, gameID = BAS.random_game('both')

     elif usermode == FREE_RANDOM_GAME :       
          gamename, gameID = BAS.random_free_game('both')

     discount = BAS.game_discount(gameID)

     print(f"\n--- {gamename.upper()} ---\n")
     print(gameID)
     print(BAS.game_description(gameID))
     print('\n')
     print(f"Developers: {BAS.game_developers(gameID)}")
     print(f"Publishers: {BAS.game_publishers(gameID)}")
     print(f"\nNeed help? Check out this ==> {' , '.join(BAS.game_support(gameID))}")
     print(f"Comming soon? {BAS.release_date(gameID, return_comming_soon = True)}, When? {BAS.release_date(gameID)}")

     if discount != 0 and isinstance(discount, int):
          print(f"\nPrice: {BAS.game_price(gameID)} with {discount}% discount")
     else:
          print(f"\nPrice: {BAS.game_price(gameID)}")


#NOTE          
# In recent Python release, 3.10 from 2021, there is a new function called "match-case" which is equivelent to "switch-case" 
# from C family, however it is not currently avaiable for Ubuntu 20+ which I'm currently using, 
# and therfore the code is not optimized at its fullest potential. 
# This will change in the future update when I will have access to Python 3.10.
    