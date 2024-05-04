# 18:07
from typing_extensions import ParamSpecArgs

from settings import *

import discord
import asyncio
import random
from itertools import cycle

class RussianRoulette:
    name = "Russian Roulette"
    icon = I_REVOLVER
    def __init__(self, bot, ctx, player1, player2, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player1 = player1
        self.player2 = player2
        self.bet = bet
        self.currency = currency
        self.players = [player1, player2]
        self.player_turns = cycle(self.players)

    async def start_game(self):
        bullet_in = random.randint(1, 6)        
        current_turn = next(self.player_turns)
        for i in range(1, 7):
            chambers = 6 - (i - 1)
            interval = random.randint(5, 15)
            await self.ctx.send(f"{(E_BULLET) * chambers}\n{chambers} chambers left and {current_turn.mention} pulls the trigger {E_REVOLVER}...")
            await asyncio.sleep(interval)
            if i == bullet_in:
                await self.ctx.send(f"**BANG**! {current_turn.mention} dies!")
                await asyncio.sleep(1)
                break
            
            current_turn = next(self.player_turns)
            await self.ctx.send(f"click! Nothing happens.\nIt's now {current_turn.mention}'s turn.")
            await asyncio.sleep(1)

        current_turn = next(self.player_turns)
        string = f"{current_turn.mention} survives and wins"

        if self.bet:
            await self.bot.db.add_balance(current_turn.id, self.bet * 2, self.currency.name)
            string += f" {self.bet}{self.currency.emoji}"

        string += "!"
        await self.ctx.send(string)

class BotRussianRoulette:
    name = "Russian Roulette"
    icon = I_REVOLVER
    def __init__(self, bot, ctx, player, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player = player
        self.bet = bet
        self.currency = currency
        self.players = ["You", "I"]
        self.player_turns = cycle(self.players)

    async def start_game(self):
        bullet_in = random.randint(1, 6)        
        current_turn = next(self.player_turns)
        for i in range(1, 7):
            chambers = 6 - (i - 1)
            interval = random.randint(5, 15)
            await self.ctx.send(f"{(E_BULLET) * chambers}\n{chambers} chambers left and {current_turn} pull the trigger {E_REVOLVER}...")
            await asyncio.sleep(interval)
            if i == bullet_in:
                await self.ctx.send(f"**BANG**! {current_turn} die!")
                await asyncio.sleep(1)
                break
            
            current_turn = next(self.player_turns)
            if current_turn == "You":
                pronoun = "your"
            else:
                pronoun = "my"

            await self.ctx.send(f"click! Nothing happens.\nIt's now {pronoun} turn.")
            await asyncio.sleep(1)
            
        
        current_turn = next(self.player_turns)

        if current_turn == "You":
            await self.bot.db.add_balance(self.player.id, self.bet, self.currency.name)
            string = f"You survive and win {self.bet}{self.currency.emoji}!"
        else:
            string = f"You die and lose {self.bet}{self.currency.emoji}"

        await self.ctx.send(string)