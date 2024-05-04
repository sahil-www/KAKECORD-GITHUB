from settings import *
from game_engines import rockpaperscissors, tictactoe

# Errors
# Amount
class InvalidAmount(Exception):
    pass
class NegativeAmount(Exception):
    pass
# Currency
class CurrencyNotProvided(Exception):
    pass
class InvalidCurrency(Exception):
    pass


class Currency:
    def __init__(self, name, emoji, local):
        self.name = name
        self.emoji = emoji
        self.local = local

def number_convertor(value):
    if value:
        try:
            value = value.lower()

            # Determine multiplier
            multiplier = 1
            if value.endswith('k'):
                multiplier = 1000
                value = value[0:len(value)-1] # strip multiplier character
            elif value.endswith('m'):
                multiplier = 1000000
                value = value[0:len(value)-1] # strip multiplier character

            # convert value to float, multiply, then convert the result to int
            amount = int(float(value) * multiplier)
        except Exception:
            raise InvalidAmount

        if amount < 0:
            raise NegativeAmount
        if amount == 0:
            return

        return amount
    else:
        return

def currency_convertor(string):
    if string:
        string = string.lower()
        if (string == "kc" or string.startswith("kake")):
            return Currency("kakechips", E_KAKECHIPS, True)
        if (string == "oc" or string.startswith("owo")):
            return Currency("owochips", E_OWOCHIPS, False)
        else:
            raise InvalidCurrency
    else:
        raise CurrencyNotProvided

def time_convertor(seconds):
    seconds = int(seconds)
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return hour, minutes, seconds

def minutes_convertor(seconds):
    seconds = seconds
    sec = seconds % 60
    minutes = (seconds - sec) / 60
    time_string = ""
    if minutes != 0:
        time_string += f"**{int(minutes)} minutes** & "
    time_string += f"**{int(sec)} seconds**"
    return time_string




# Currently not in use
"""async def game_convertor(game, bot, ctx, player1, player2, bet, currency):
    game = game.lower()
    # First checks
    if game == None:
        raise GameNotProvided
    if not (game == "rps" or game.startswith("rockpaperscissor") or (game == "ttt" or game == "tictactoe")):
        raise InvalidGame

    # Managing the players
    if player2 == None:
        raise OpponentNotGiven
    if player1.id == player2.id:
        raise CantChallengeSelf
    
    # Managing the bet
    bet = number_convertor(bet)
    if bet:
        currency = currency_convertor(currency)
        await bot.db.subtract_balance(player1.id, bet, currency)
    
    # Making the game
    if (game == "rps" or game.startswith("rockpaperscissor")):
        return rockpaperscissors.RockPaperScissors(bot, ctx, player1, player2, bet, currency), bet
    else: # (game == "ttt" or game == "tictactoe"):
        return tictactoe.TicTacToe(bot, ctx, player1, player2, bet, currency), bet
        
        
    # Its errors
    # Game
    class InvalidGame(Exception):
        pass
    class GameNotProvided(Exception):
        pass
    # Other
    class OpponentNotGiven(Exception):
        pass
    class CantChallengeSelf(Exception):
        pass"""