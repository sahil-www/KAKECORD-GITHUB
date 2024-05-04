from settings import *
import discord
import asyncio

from random import randint

class CoinFlip:
    name = "Coin Flip"
    icon = I_COINFLIP
    def __init__(self, bot, ctx, player1, player2, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player1 = player1
        self.player2 = player2
        self.bet = bet
        self.currency = currency

    async def start_game(self):
        msg_string = f"{self.player1.mention} chose Heads {E_HEADS}\n{self.player2.mention} chose Tails {E_TAILS}\nThe coin spins... "
        msg = await self.ctx.send(f"{msg_string}{E_COINFLIP}")
        winner = randint(0, 1)
        await asyncio.sleep(5)
        if winner == 0:
            msg_string += f"{E_HEADS}, {self.player1.mention} wins"
            winner = self.player1
        else:
            msg_string += f"{E_TAILS}, {self.player2.mention} wins"
            winner = self.player2
        if self.bet:
            await self.bot.db.add_balance(winner.id, self.bet * 2, self.currency.name)
            msg_string += f" {self.bet}{self.currency.emoji}"
        
        msg_string += "!"
        await msg.edit(content=msg_string)

# WIP
class BotCoinFlip:
    name = "Coin Flip"
    icon = I_COINFLIP
    def __init__(self, bot, ctx, player, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player = player
        self.bet = bet
        self.currency = currency

    async def start_game(self):
        msg_string = f"{self.player.mention}, yours is Heads {E_HEADS}\nMine is Tails {E_TAILS}\nThe coin spins... "
        msg = await self.ctx.send(f"{msg_string}{E_COINFLIP}")
        winner = randint(0, 1)
        await asyncio.sleep(5)
        if winner == 0:
            msg_string += f"{E_HEADS}, you win"
            await self.bot.db.add_balance(self.player.id, self.bet * 2, self.currency.name)
        else:
            msg_string += f"{E_TAILS}, I win"

        msg_string += f" {self.bet}{self.currency.emoji}!"
        await msg.edit(content=msg_string)
    