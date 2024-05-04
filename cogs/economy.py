from discord.ext.commands.cooldowns import BucketType
from discord.ext.commands.errors import UserNotFound
from errors.database_errors import InsufficientBalance
from settings import *

import discord
from discord.ext import commands
from utils import CurrencyNotProvided, InvalidAmount, InvalidCurrency, NegativeAmount, minutes_convertor, number_convertor, currency_convertor

from random import randint

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    ################################################### ERRORS #####################################################
    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        # Common errors
        if isinstance(error, NegativeAmount):
            await ctx.send(f"{ctx.author.mention}, you can't give in negative wtf! Do you want some ass kicking?")
            return
        if isinstance(error, InsufficientBalance):
            await ctx.send(f"{ctx.author.mention}, you don't even have that much.")
            return

        # Command-specific errors
        if ctx.command == self.work:
            if isinstance(error, commands.CommandOnCooldown):
                retry = minutes_convertor(error.retry_after)
                await ctx.send(f"You can't work again for {retry}.")
                return
            else:
                await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")
                return

        else: # if ctx.command == self.give:
            # footer = ""        # Default footer value, as not every error message will have a footer         # For now not using footers
            if isinstance(error, UserNotFound):
                description = "**Invalid <user> provided**\n\nUsage:\n`<prefix>give <user> <amount> <chips>`\n> Either @mention the user or provide their ID."
            elif isinstance(error, InvalidAmount):
                description = "**Invalid <amount> provided**\n\nUsage:\n`<prefix>give <user> <amount> <chips>`"
            elif isinstance(error, CurrencyNotProvided):
                description = "**<chips> not provided**\n\nUsage:\n`<prefix>give <user> <amount> <chips>`"
            elif isinstance(error, InvalidCurrency):
                description = "**Invalid <chips> provided**\n\nUsage:\n`<prefix>give <user> <amount> <chips>`"
            else:
                await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")
                return

            # The embed will be created and then sent
            embed = discord.Embed(
                    description = description,
                    colour = 0xFF0000
                )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            # embed.set_footer(text=footer")
            await ctx.send(embed=embed)    
            #elif <different command>
            return

    ################################################################################################################
    
    # THIS COMMAND WORKS PROPERLY
    # Possible errors: 1. UserNotFound 2. InvalidAmount, 3. NegativeAmount, 4. CurrencyNotProvided, 5. InvalidCurrency, 6. InsufficientBalance
    @commands.command(name="give")
    @commands.guild_only()
    async def give(self, ctx, user : discord.User = None, amount=None, currency=None):
        if user == None or amount == None or currency == None:
            embed = discord.Embed(
                description = "**Provide all arguments**\n\nUsage:\n`<prefix>give <amount> <chips>`",
                colour = 0xFF0000
            )
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return
        if user == ctx.author:
            await ctx.send("You can't give your chips to yourself, what're you thinking?")
            return
        amount = number_convertor(amount)
        if amount == None:
            await ctx.send("If you don't have money then don't try to be generous.")
            return
        currency = currency_convertor(currency.lower())
        await self.bot.db.check_presence(ctx.author.id)
        await self.bot.db.check_presence(user.id)
        await self.bot.db.give_money(ctx.author.id, user.id, amount, currency.name)
        await ctx.send(f"{amount}{currency.emoji} given to {user.mention} by {ctx.author.mention}")

    @commands.command(name="work")
    @commands.guild_only()
    @commands.cooldown(rate=1, per=3600, type=BucketType.user)
    async def work(self, ctx):
        amount = randint(40, 60)
        string = f"{ctx.author.mention}, you earned {amount}{E_KAKECHIPS} by working."
        """if ctx.author.has_role(self.bot.server_booster_role):
                                    increased = randint(6, 10)
                                    string += f" You earned a bonus of {amount}{E_KAKECHIPS} for boosting the server."
                                    amount += increased"""

        await self.bot.db.check_presence(ctx.author.id)
        await self.bot.db.add_balance(ctx.author.id, amount, "kakechips")
        await ctx.send(string)


def setup(bot):
    bot.add_cog(Economy(bot))