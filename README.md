# bettersteamapi

[![license](https://img.shields.io/github/license/netW3k/bettersteamapi)](https://github.com/netW3k/bettersteamapi/blob/GitInit/LICENSE)
[![issues](https://img.shields.io/github/issues/netW3k/bettersteamapi)](https://github.com/netW3k/bettersteamapi/issues)

A set of functions to easily access game data such as price of the game, discount percentage (if the game is on discount), release date and more!

*bettersteamapi* is a package you want to use when you want to work with steam games, no matter if it is a full-scale project with a colorfull GUI, or if your are working on a simple Python script to to get all games on discount in real-time.

Gain access to prices, discounts, and a special game roulette!

Tested on Python 3.8 and 3.9 on Ubuntu 20.04 (Python 3.10 is not yet officially released on Ubuntu 20.04)


WORK IN PROGRESS

## Installation

>`pip install -U bettersteamapi`

For more information see the [documentation]().

## Help
See [documentation]() for more details about functions and how they work. 

## Example
I have created a simple example that prints out basic information of the typed game. In addition, the example file shows how you can use special function *random_game* and *random_free_game*. 

Here is a basic example of how to use *validate_game* and *get_game_price* functions.
```py
import bettersteamapi.steamfunctions as bas

gameid = bas.validate_game(game = 'dead by daylight', return_gameid = True)
print(bas.get_game_price(gameid = gameid))
#> $19.99 USD (fixed price)

```

Check out full [example](https://github.com/netW3k/bettersteamapi/blob/GitInit/example.py).
