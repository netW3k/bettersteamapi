import functions as BAS

usermode = ''
gameinfo = '1'
randomgame = '2'
freerandomgame = '3'
exit = '4'


while usermode != exit:

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

          if usermode == gameinfo or usermode == randomgame or usermode == freerandomgame or usermode == exit: 
               validInput = True # <Not ideal way of checking user input, however it serves its purpose>
     
     if usermode == exit : break

     if usermode == gameinfo : 
          
          exists = False
          
          while not exists:
               
               gamename = input('What is the name of the game? ')
               
               if BAS.validateGame(gamename) is True:
                   
                    gameID = BAS.validateGame(gamename, True)
                    exists = True

     elif usermode == randomgame : 
          gamename, gameID = BAS.randomGame('both')

     elif usermode == freerandomgame :       
          gamename, gameID = BAS.randomFreeGame('both')

     discount = BAS.gameDiscount(gameID)

     print(f"\n--- {gamename.upper()} ---\n")
     print(BAS.gameDesc(gameID))
     print('\n')
     print(f"Developers: {BAS.gameDev(gameID)}")
     print(f"Publishers: {BAS.gamePub(gameID)}")
    
     if discount != 0 and isinstance(discount, int):
          print(f"\nPrice: {BAS.gamePrice(gameID)} with {discount}% discount")
     else:
          print(f"\nPrice: {BAS.gamePrice(gameID)}")


#NOTE          
# In recent Python release, 3.10 from 2021, there is a new function called "match-case" which is equivelent to "switch-case" 
# from C family, however it is not currently avaiable for Ubuntu 20+ which I'm currently using, 
# and therfore the code is not optimized at its fullest potential. 
# This will change in the future update when I will have access to Python 3.10.
    