from settings import *
import discord
import asyncio

from random import choice

class RockPaperScissors:
    name = "Rock Paper Scissors"
    icon = I_RPS
    def __init__(self, bot, ctx, player1, player2, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player1 = player1
        self.player2 = player2
        self.bet = bet
        self.currency = currency

    async def start_game(self):
        p1embed = discord.Embed(title=f"Rock Paper Scissors", description=f"Choose what you'd like to use against {self.player2}", colour=0xFF0000)
        p2embed = discord.Embed(title=f"Rock Paper Scissors", description=f"Choose what you'd like to use against {self.player1}", colour=0xFF0000)
        p1embed.set_footer(text="Use `<prefix>instructions rockpapscissors` for instructions.")
        p2embed.set_footer(text="Use `<prefix>instructions rockpapscissors` for instructions.")
        slctd = []
        p1msg = await self.player1.send(embed=p1embed)
        p2msg = await self.player2.send(embed=p2embed)

        await p1msg.add_reaction(E_ROCK)
        await p2msg.add_reaction(E_ROCK)
        await p1msg.add_reaction(E_PAPER)
        await p2msg.add_reaction(E_PAPER)
        await p1msg.add_reaction(E_SCISSORS)
        await p2msg.add_reaction(E_SCISSORS)

        def check(reaction, user):
            return (
                (reaction.message.id == p1msg.id or
                reaction.message.id == p2msg.id) and
                (user == self.player1 or
                user == self.player2) and
                (str(reaction.emoji) == E_ROCK or
                str(reaction.emoji) == E_PAPER or
                str(reaction.emoji) == E_SCISSORS) and
                user not in slctd
            )
        # Waiting for the players' reactions
        try:
            reaction1, user1 = await self.bot.wait_for("reaction_add", timeout=30, check=check)
            slctd.append(user1)
            await user1.send(f"You selected {reaction1.emoji}")

            reaction2, user2 = await self.bot.wait_for("reaction_add", timeout=30, check=check)
            slctd.append(user2)
            await user2.send(f"You selected {reaction2.emoji}")

        # If someone fails to react on time
        except asyncio.TimeoutError:
            if self.player1 not in slctd:
                if self.player2 not in slctd:
                    timeout_string = (f"Game cancelled, {self.player1.mention} and {self.player2.mention} both failed to react on time.")
                else:
                    timeout_string = (f"Game cancelled, {self.player1.mention} failed to react on time.")
            else:
                timeout_string = (f"Game cancelled, {self.player2.mention} failed to react on time.")

            if self.bet:
                await self.bot.db.add_balance(self.player1.id, self.bet, self.currency.name)
                await self.bot.db.add_balance(self.player2.id, self.bet, self.currency.name)
                timeout_string += " The bet has been returned to both of the players."
                
            await self.ctx.send(timeout_string)
            return

        # After both of the players have reacted, checking the winner
        winner, colour, image = await self.winner_check(user1, user2, str(reaction1), str(reaction2))
        
        # After Calculation
        embed = discord.Embed(title="Rock Paper Scissors", description=f"{user1.mention} {E_VS} {user2.mention}", colour=colour)

        # Generating the result strings and doing the necesarry tasks
        # If there is a winner
        if winner:
            result_string = f"{user1.name} selected {reaction1} and {user2.name} selected {reaction2}\n**{winner.name} wins"
            if self.bet:
                await self.bot.db.add_balance(winner.id, self.bet * 2, self.currency.name)
                result_string += f" {self.bet}{self.currency.emoji}"
            result_string += "!**"
        
        # If there is no winner, i.e. a draw
        else:
            result_string = f"Both selected {reaction1}\n**It's a draw!**"
            if self.bet:
                await self.bot.db.add_balance(user1.id, self.bet, self.currency.name)
                await self.bot.db.add_balance(user2.id, self.bet, self.currency.name)
                result_string += "\nBoth of the players take back their bets."
        
        embed.set_thumbnail(url=image)
        embed.add_field(name="Result", value=result_string)
        await self.ctx.send(embed=embed)

    # Will return 3 variables, winner, colour and the image url. If its a draw, winner will be None
    async def winner_check(self, p1, p2, r1, r2):
        c_rock = 0xef5480
        c_paper = 0xffde55
        c_scissors = 0x74dae2
        if r1 == r2:
            if r1 == E_ROCK:
                return None, c_rock, I_ROCK
            elif r1 == E_PAPER:
                return None, c_paper, I_PAPER
            else:
                return None, c_scissors, I_SCISSORS

        elif r1 == E_ROCK:
            if r2 == E_PAPER:
                return p2, c_paper, I_PAPER               # Paper beats Rock
            else:
                return p1, c_rock, I_ROCK                # Can't be Rock, Scissors left

        elif r1 == E_PAPER:
            if r2 == E_SCISSORS:
                return p2, c_scissors, I_SCISSORS            # Scissors beats Paper
            else:
                return p1, c_paper, I_PAPER               # Can't be paper, Rock left
            
        else:
            if r2 == E_ROCK:
                return p2, c_rock, I_ROCK                # Rock beats Scissors
            else:
                return p1, c_scissors, I_SCISSORS            # Can't be Scissors, Paper left


class BotRockPaperScissors:
    name = "Rock Paper Scissors"
    icon = I_RPS
    def __init__(self, bot, ctx, player, bet, currency):
        self.bot = bot
        self.ctx = ctx
        self.player = player
        self.bet = bet
        self.currency = currency
    
    async def start_game(self):
        embed = discord.Embed(
            title=f"Rock Paper Scissors",
            description=f"{self.player.mention}, choose what you'd like to use against me.",
            colour=0xFF0000
        )
        embed.set_thumbnail(url=I_RPS)
        embed.set_footer(text="Use `<prefix>instructions rockpapscissors` for instructions.")
        msg = await self.ctx.send(embed=embed)
        await msg.add_reaction(E_ROCK)
        await msg.add_reaction(E_PAPER)
        await msg.add_reaction(E_SCISSORS)

        reactions = [E_ROCK, E_PAPER, E_SCISSORS]

        def check(reaction, user):
            return (
                reaction.message.id == msg.id and
                user == self.player and
                str(reaction.emoji) in reactions
            )

        # Waiting for the players' reactions
        try:
            playerreaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)
        # If they fail to react on time
        except asyncio.TimeoutError:
            await self.bot.db.add_balance(self.player.id, self.bet, self.currency.name)
            await self.ctx.send(f"You failed to react on time. Your bet has been returned.")
            return
        
        botreaction = choice(reactions)
        winner, colour, image = await self.winner_check(self.player, "Me", str(playerreaction), str(botreaction))
        embed = discord.Embed(title="Rock Paper Scissors", description=f"{self.player.mention} {E_VS} Me", colour=colour)
        
        # If the  player wins
        if winner == self.player:
            await self.bot.db.add_balance(winner.id, self.bet * 2, self.currency.name)
            result_string = f"{self.player.name}, You selected {playerreaction} and I selected {botreaction}\n**You win {self.bet}{self.currency.emoji}!**"
        # If there is no winner, i.e. a draw
        elif winner == None:
            await self.bot.db.add_balance(self.player.id, self.bet, self.currency.name)
            result_string = f"{self.player.mention}, we both selected {playerreaction}\n**It's a draw!**\nYour bet has been returned."
        else:
            result_string = f"{self.player.name}, You selected {playerreaction} and I selected {botreaction}\n**I win {self.bet}{self.currency.emoji}!**"

        embed.set_thumbnail(url=image)
        embed.add_field(name="Result", value=result_string)
        await msg.edit(embed=embed)
        
    # Will return 3 variables, winner, colour and the image url. If its a draw, winner will be None (Similar to the winner_check of RockPaperScissors above)
    async def winner_check(self, p1, p2, r1, r2):
        c_rock = 0xef5480
        c_paper = 0xffde55
        c_scissors = 0x74dae2
        if r1 == r2:
            if r1 == E_ROCK:
                return None, c_rock, I_ROCK
            elif r1 == E_PAPER:
                return None, c_paper, I_PAPER
            else:
                return None, c_scissors, I_SCISSORS

        elif r1 == E_ROCK:
            if r2 == E_PAPER:
                return p2, c_paper, I_PAPER               # Paper beats Rock
            else:
                return p1, c_rock, I_ROCK                # Can't be Rock, Scissors left

        elif r1 == E_PAPER:
            if r2 == E_SCISSORS:
                return p2, c_scissors, I_SCISSORS            # Scissors beats Paper
            else:
                return p1, c_paper, I_PAPER               # Can't be paper, Rock left
            
        else:
            if r2 == E_ROCK:
                return p2, c_rock, I_ROCK                # Rock beats Scissors
            else:
                return p1, c_scissors, I_SCISSORS            # Can't be Scissors, Paper left