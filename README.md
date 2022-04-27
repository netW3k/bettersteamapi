# bettersteamapi

[![license](https://img.shields.io/github/license/netW3k/bettersteamapi)](https://github.com/netW3k/bettersteamapi/blob/GitInit/LICENSE)
[![issues](https://img.shields.io/github/issues/netW3k/bettersteamapi)](https://github.com/netW3k/bettersteamapi/issues)

A set of functions to easily access game data (game price, name of the game, release date, etc), if the game is on discount, or get the name of developers of the game! 

*bettersteamapi* is a package you want to use when you want to work with steam games, no matter if it is a full-scale project with colorfull GUI, or a simple Python script to access all the games on discount.

Gain access to prices, discounts, and a special game roulette!

Tested on Python 3.8 and 3.9 on Ubuntu 20.04 (Python 3.10 is not yet officially released on Ubuntu 20.04)


## Installation

>`pip install -U bettersteamapi`

For more information see the [Install]().

## Help
See [documentation]() for more details about functions and how they work. 

## Example
I have created a simple example that prints out basic information of the typed game. In addition, the example file shows how you can use special function *random_game* and *random_free_game*. 

Here is a basic example of how to use *validate_game* and *get_game_price* functions.
```py
from steamfunctions import validate_game, get_game_price

gameid = validate_game('dead by daylight', True)
print(get_game_price(gameid))
#> $19.99 USD

```

Check out full [example](https://github.com/netW3k/bettersteamapi/blob/GitInit/example.py).
