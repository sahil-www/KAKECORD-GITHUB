from typing import OrderedDict, Text
from discord import team
from discord.ext.commands.converter import EmojiConverter
from settings import *

import discord
from discord.ext import commands
import asyncio
from utils import number_convertor, currency_convertor

# Game Engines
from game_engines.rockpaperscissors import RockPaperScissors, BotRockPaperScissors
from game_engines.tictactoe import TicTacToe
from game_engines.coinflip import CoinFlip, BotCoinFlip
from game_engines.blackjack import BotBlackjack
from game_engines.russianroulette import RussianRoulette, BotRussianRoulette

# Importing errors
from discord.ext.commands.errors import MemberNotFound
from databasehelper import InsufficientBalance
from utils import InvalidAmount, NegativeAmount, CurrencyNotProvided, InvalidCurrency

class Gamble(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help = self.bot.get_cog("Help")

    ################################################ ERRORS ########################################################

    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        # Common errors
        if isinstance(error, InsufficientBalance):        # For the first insufficient balance error that occurs before the challenge message is sent, the one that occurs when player tries accepting the challenge is handeled within the function using try except blocks.
            await ctx.send("You don't even have that much.")
            return
        if isinstance(error, NegativeAmount):
            await ctx.send("You can't bet in negative! Don't try to cheat!")
            return

        # Command-specific errors
        if ctx.command == self.challenge:
            if isinstance(error, MemberNotFound):
                embed = discord.Embed(
                    description = "**Invalid <opponent> provided**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> Either @mention the user or provide their ID.",
                    colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="The user must be a member of this server.")
                await ctx.send(embed=embed)
                return
            if isinstance(error, InvalidAmount):
                embed = discord.Embed(
                    description = "**Invalid <bet> provided**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> You have to provide `<chips>` if you provide `<bet>`.",
                    colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="The arguments after `|` are optional.")
                await ctx.send(embed=embed)
                return
            if isinstance(error, CurrencyNotProvided):
                embed = discord.Embed(
                description = "**<chips> not provided**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> You have to provide `<chips>` if you provide `<bet>`.",
                colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="The arguments after `|` are optional.")
                await ctx.send(embed=embed)
                return
            if isinstance(error, InvalidCurrency):
                embed = discord.Embed(
                description = "**Invalid <chips> provided**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> You have to provide `<chips>` if you provide `<bet>`.",
                colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="The arguments after `|` are optional.")
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")
        
        else: # if ctx.command == self.botchallenge:
            if isinstance(error, InvalidAmount):
                embed = discord.Embed(
                    description = "**Invalid <bet> provided**\n\nUsage:\n`<prefix>botchallenge <game> <bet> <chips>`",
                    colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if isinstance(error, CurrencyNotProvided):
                embed = discord.Embed(
                description = "**<chips> not provided**\n\nUsage:\n`<prefix>botchallenge <game> <bet> <chips>`",
                colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            if isinstance(error, InvalidCurrency):
                embed = discord.Embed(
                description = "**Invalid <chips> provided**\n\nUsage:\n`<prefix>botchallenge <game> <bet> <chips>`",
                colour = 0xFF0000
                )
                embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")
    ################################################################################################################
    # Possible errors: 1. MemberNotFound, 2. InvalidAmount, 3. NegativeAmount, 4. CurrencyNotProvided, 5. InvalidCurrency, 6. InsufficientBalance
    # This can be optimized but not with my level of knowledge
    @commands.command(name="challenge", aliases=["ch"])
    @commands.guild_only()                      # 1                                                         (1) Can throw MemberNotFound error
    async def challenge(self, ctx, game=None, opponent: discord.Member=None, bet=None, currency=None):
        # First checks
        if game == None or opponent == None:
            embed = discord.Embed(
                description = "**Provide all arguments**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> Choose a game from `<prefix>games challenge`",
                colour = 0xFF0000
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="The arguments after `|` are optional.")
            await ctx.send(embed=embed)
            return
        game = game.lower()
        if not ((game == "rps" or game.startswith("rockpaperscissor")) or (game == "ttt" or game == "tictactoe") or (game == "rr" or game == "russianroulette") or (game == "cf" or game == "coinflip")):
            embed = discord.Embed(
                description = "**Invalid <game> provided**\n\nUsage:\n`<prefix>challenge <game> <opponent> | <bet> <chips>`\n> Choose a game from `<prefix>games challenge`",
                colour = 0xFF0000
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="The arguments after `|` are optional.")
            await ctx.send(embed=embed)
            return

        # The opponent shouldn't be the author themselves
        if ctx.author.id == opponent.id:
            await ctx.send("You can't challenge yourself.")
            return
        
        # Now as the players are managed, it won't throw any error
        await self.bot.db.check_presence(ctx.author.id)
        await self.bot.db.check_presence(opponent.id)

        # Managing the bet
        bet = number_convertor(bet)        # Can throw 1. InvalidAmount, 2. NegativeAmount
        if bet:
            currency = currency_convertor(currency)     # Can throw 1. CurrencyNotProvided, 2. InvalidCurrency errors
            await self.bot.db.subtract_balance(ctx.author.id, bet, currency.name)        # Can throw 1. InsufficientBalance error
        
        # Making the game
        if (game == "rps" or game.startswith("rockpaperscissor")):
            game = RockPaperScissors(self.bot, ctx, ctx.author, opponent, bet, currency)
        elif (game == "ttt" or game == "tictactoe"):
            game = TicTacToe(self.bot, ctx, ctx.author, opponent, bet, currency)
        elif (game == "rr" or game == "russianroulette"):
            game = RussianRoulette(self.bot, ctx, ctx.author, opponent, bet, currency)
        else: # (game == "cf" or game == "coinflip"):
            game = CoinFlip(self.bot, ctx, ctx.author, opponent, bet, currency)
        
        # This is the part where the challenge message is customized and sent
        # If there is a bet or not
        if bet:
            challenge_title = "Challenge"
            challenge_description = f"{opponent.mention}, you are being challenged by {ctx.author.mention}\nPress {E_CHECK} to accept and match the bet or {E_CROSS} to decline."
            challenge_bet = f"{bet}{currency.emoji}"
        else:
            challenge_title = "Friendly Challenge"
            challenge_description = f"{opponent.mention} you are being challenged by {ctx.author.mention}\nPress {E_CHECK} to accept or {E_CROSS} to decline."
            challenge_bet = "None"

        # The message is created and sent here
        embed = discord.Embed(
                title=challenge_title,
                description=challenge_description,
                colour=0xFF0000
            )
        embed.add_field(name="Game", value=game.name)
        embed.add_field(name="Bet", value=challenge_bet)
        embed.set_thumbnail(url=game.icon)
        challenge_msg = await ctx.send(embed=embed)
        await challenge_msg.add_reaction(E_CHECK)
        await challenge_msg.add_reaction(E_CROSS)
        
        # Here is the reaction part
        def check(reaction, user):
            return (
                challenge_msg.id == reaction.message.id and
                user == opponent and
                str(reaction.emoji) in [E_CHECK, E_CROSS]
            )        # Defining the check

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30, check=check)

            # If reaction is check
            if str(reaction.emoji) == E_CHECK:
                if bet:
                    try:
                        await self.bot.db.subtract_balance(opponent.id, bet, currency.name)
                    except Exception:
                        await self.bot.db.add_balance(ctx.author.id, bet, currency.name)
                        await ctx.send(f"Challenge has been cancelled, {opponent.mention} doesn't have enough {currency.emoji} to accept this challenge\n{ctx.author.mention} your bet has been returned.")
                        return

                # Game is started, if there was a bet, it will be handeled above
                await ctx.send("Challenge accepted!")
                await asyncio.sleep(1)
                await game.start_game()
                return        # I would want the command to return after the game has completed

            # If reaction is cross
            elif str(reaction.emoji) == E_CROSS:
                message_string = f"{ctx.author.mention}, {opponent.mention} has declined your challenge."
                if bet:
                    await self.bot.db.add_balance(ctx.author.id, bet, currency.name)
                    message_string += " Your bet has been returned."
                await ctx.send(message_string)

        except asyncio.TimeoutError:
            message_string = f"{ctx.author.mention}, your challenge expired."
            if bet:
                await self.bot.db.add_balance(ctx.author.id, bet, currency.name)
                message_string += " Your bet has been returned."
            await ctx.send(message_string)

    # Possible errors: 1. InvalidAmount, 2. NegativeAmount, 3. CurrencyNotProvided 4. InvalidCurrency, 5. InsufficientBalance
    @commands.command(name="botchallenge", aliases=["bch"])
    @commands.guild_only()
    async def botchallenge(self, ctx, game = None, bet = None, currency = None):
        # First checks
        if game == None or bet == None or currency == None:
            embed = discord.Embed(
                description = "**Provide all arguments**\n\nUsage:\n`<prefix>botchallenge <game> <bet> <chips>`\n> Choose a game from `<prefix>games botchallenge`",
                colour = 0xFF0000
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="I don't play without a bet.")
            await ctx.send(embed=embed)
            return
        
        # Converting
        game = game.lower()
        # Checking if the game is available
        if not ((game == "bj" or game == "blackjack") or (game == "rr" or game == "russianroulette") or (game == "rps" or game.startswith("rockpaperscissor")) or (game == "cf" or game == "coinflip")):
            embed = discord.Embed(
                description = "**Invalid <game> provided**\n\nUsage:\n`<prefix>botchallenge <game> <bet> <chips>`\n> Choose a game from `<prefix>games botchallenge`",
                colour = 0xFF0000
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return

        # Converting the bet
        bet = number_convertor(bet)
        if bet:        # Can throw 1. InvalidAmount, 2. NegativeAmount errors
            currency = currency_convertor(currency)        # Can throw 1. InvalidCurrency error
            # Prevents people from betting other bots' currency
            if currency.local == False:
                await ctx.send(f"You can't bet {currency.emoji} against me, these chips can only be wagered against others.")
                return
            await self.bot.db.subtract_balance(ctx.author.id, bet, currency.name)        # Can throw 1. InsufficientBalance error
        else:
            await ctx.send("I don't play with no money.")
            return
        
        await self.bot.db.check_presence(ctx.author.id)
        # Making the game
        if (game == "bj" or game == "blackjack"):
            game = BotBlackjack(self.bot, ctx, ctx.author, bet, currency)
        elif (game == "rr" or game == "russianroulette"):
            game = BotRussianRoulette(self.bot, ctx, ctx.author, bet, currency)
        elif (game == "rps" or game.startswith("rockpaperscissor")):
            game = BotRockPaperScissors(self.bot, ctx, ctx.author, bet, currency)
        else: # (game == "cf" or game == "coinflip"):
            game = BotCoinFlip(self.bot, ctx, ctx.author, bet, currency)
        
        await ctx.send("I accept your challenge!")
        await asyncio.sleep(1)
        await game.start_game()

    ############################################## GAMES COMMAND ###################################################

    @commands.group(name="games", aliases=["game", "gambling", "gamble"], case_insensitive=True, invoke_without_command=True)
    async def games(self, ctx):
        embed = discord.Embed(
            title="<prefix>games",
            description="View the list of available games for a particular category.\nAvailable categories:\n> challenge\n> botchallenge",
            colour=0XFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>games <category>`")
        embed.add_field(name="Alias", value="`game`, `gambling`, `gamble`")
        embed.set_footer(text="Although new games are constantly being added into Kakecord, it can't do much due to the lack of funds, please consider supporting Kakecord using `<prefix>support` if you can.")
        await ctx.send(embed=embed)
    
    @games.command(name="challenge", aliases=["ch", "challenges"])
    async def games_challenge(self, ctx):
        embed = discord.Embed(
            title = "Available Games for <prefix>challenge",
            description = 
            """This is the list of available games you can play against other players, _more games coming soon._
            To play, use `<prefix>challenge <game> <opponent> | <bet> <chips>`
            To view the instructions, use `<prefix>instructions <game>`""",
            colour = 0xFF0000
        )
        embed.add_field(name="Rock Paper Scissors", value="ID: `rockpaperscissors` or `rockpaperscissor` or `rps`", inline=False)
        embed.add_field(name="Tic Tac Toe", value="ID: `tictactoe` or `ttt`", inline=False)
        embed.add_field(name="Coin Flip", value="ID: `coinflip` or `cf`", inline=False)
        embed.add_field(name="Russian Roulette", value="ID: `russianroulette` or `rr`", inline=False)
        embed.set_footer(text="The arguments after `|` are optional.\nThe ID of the game is required in the `<game>` parameter of the commands.")
        await ctx.send(embed=embed)
        
    @games.command(name="botchallenge", aliases=["bch", "botchallenges"])
    async def games_botchallenge(self, ctx):
        embed = discord.Embed(
            title = "Available Games for <prefix>botchallenge",
            description = 
            """This is the list of available games you can play against me, _more games coming soon._
            To play, use `<prefix>botchallenge <game> <bet> <chips>`
            To view the instructions, use `<prefix>instructions <game>`""",
            colour = 0xFF0000
        )
        embed.add_field(name="Rock Paper Scissors", value="ID: `rockpaperscissors` or `rockpaperscissor` or `rps`", inline=False)
        embed.add_field(name="Coin Flip", value="ID: `coinflip` or `cf`", inline=False)
        embed.add_field(name="Blackjack", value="ID: `blackjack` or `bj`", inline=False)
        embed.add_field(name="Russian Roulette", value="ID: `russianroulette` or `rr`", inline=False)
        embed.set_footer(text="The ID of the game is required in the `<game>` parameter of the commands.")
        await ctx.send(embed=embed)

    ########################################### INSTRUCTIONS COMMAND ##############################################
    
    @commands.group(name="instructions", aliases=["instruction", "ins", "rule", "rules"], case_insensitive=True, invoke_without_command=True)
    async def instructions(self, ctx):
        embed = discord.Embed(
            title="<prefix>instructions",
            description=
            """View the instructions on how to play a particular game.
            Available games:
            > rockpaperscissors
            > tictactoe
            > coinflip
            > blackjack
            > russianroulette""",
            colour=0XFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>instructions <game>`")
        embed.add_field(name="Alias", value="`instruction`, `ins`, `rules`, `rule`, `help`")
        embed.set_footer(text="Although new games are constantly being added into Kakecord, it can't do much due to the lack of funds, please consider supporting Kakecord using `<prefix>support` if you can.")
        await ctx.send(embed=embed)

    @instructions.command(name="rockpaperscissors", aliases=["rockpaperscissor", "rps"])
    async def instructions_rockpaperscissors(self, ctx):
        await self.help.help_rockpaperscissors(ctx)

    @instructions.command(name="tictactoe", aliases=["ttt"])
    async def instructions_tictactoe(self, ctx):
        await self.help.help_tictactoe(ctx)

    @instructions.command(name="coinflip", aliases=["cf"])
    async def instructions_coinflip(self, ctx):
        await self.help.help_coinflip(ctx)

    @instructions.command(name="blackjack", aliases=["bj"])
    async def instructions_blackjack(self, ctx):
        await self.help.help_blackjack(ctx)

    @instructions.command(name="russianroulette", aliases=["rr"])
    async def instructions_russianroulette(self, ctx):
        await self.help.help_russianroulette(ctx)
        
def setup(bot):
    bot.add_cog(Gamble(bot))
