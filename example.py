from bettersteamapi import steamfunctions as bas

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

     if usermode == GAME_INFO: 
          exist = False

          while exist is False:
               gamename = ''
               gamename = input('What is the name of the game? ')

               if bas.validate_game(gamename) is False:
                    if not bas.game_suggestions(gamename):
                         print("No game found!")
                         continue  
                    print(bas.game_suggestions(gamename))
                    continue
                   
               gameid = bas.validate_game(gamename, True)
               exist = True

     elif usermode == RANDOM_GAME: 
          game_data = bas.get_random_game()
          gamename = game_data['name']
          gameid = game_data['appid']

     elif usermode == FREE_RANDOM_GAME :       
          game_data = bas.random_free_game()
          gamename = game_data['name']
          gameid = game_data['appid']

     print(f"\n--- {gamename.upper()} ---\n")
     print(bas.get_game_description(gameid))
     print('\n')
     print(f"Check it out --> {bas.get_store_page(gameid)}")
     print(f"\nDevelopers: {' , '.join(bas.game_developers(gameid))}")
     print(f"Publishers: {' , '.join(bas.game_publishers(gameid))}")
     print(f"\nNeed help? Check out this ==> {bas.game_support(gameid)}")
     print(f"Comming soon? {bas.get_release_date(gameid, return_comming_soon = True)}, When? {bas.get_release_date(gameid)}")

     if bas.check_if_game_on_discount(gameid):
          discount = bas.get_game_discount(gameid)
          
          print(f"\nPrice: {bas.get_game_price(gameid)} with {discount}% discount")
     else:
          print(f"\nPrice: {bas.get_game_price(gameid)}")


#NOTE          
# In recent Python release, 3.10 from 2021, there is a new function called "match-case" which is equivelent to "switch-case" 
# from C family, however it is not currently avaiable for Ubuntu 20+ which I'm currently using, 
# and therfore the code is not optimized at its fullest potential. 
# This will change in the future update when I will have access to Python 3.10.

#NOTE
#This program was intended to show roughly how different methods work together and how to use them
#in the most basic way. This showcase would be better if methods were used, but 
#I'm too lazy to do it.
