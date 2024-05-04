from settings import *

import discord
from discord.ext import commands

from utils import number_convertor, currency_convertor

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    ################################################ ERRORS #######################################################
    async def cog_command_error(self, ctx, error):
       return
    ################################################ OWNER ########################################################
    # This part hasnt been touched yet
    @commands.command(name="addchips")
    @commands.is_owner()
    async def addchips(self, ctx, user : discord.User = None, amount=None, currency=None):
        try:
            if user == None or amount == None or currency == None:
                await ctx.send("Provide me User, Amount and Chips in order for me to continue.")
                return
            amount = number_convertor(amount)
            currency = currency_convertor(currency)
            await self.bot.db.check_presence(user.id)
            await self.bot.db.add_balance(user.id, amount, currency.name)
            await ctx.send(f"Added {amount}{currency.emoji} to {user}'s account")

        except Exception:
            await ctx.send("Error occured\nUsage:\n`<prefix>addchips <user> <amount> <chips>`")

    @commands.command(name="subtractchips")
    @commands.is_owner()
    async def subtractchips(self, ctx, user : discord.User = None, amount=None, currency=None):
        try:
            if user == None or amount == None or currency == None:
                await ctx.send("Provide me User, Amount and Chips in order for me to continue.")
                return
            amount = number_convertor(amount)
            currency = currency_convertor(currency)
            await self.bot.db.check_presence(user.id)
            await self.bot.db.subtract_balance(user.id, amount, currency.name)
            await ctx.send(f"Subtracted {amount}{currency.emoji} from {user}'s account")
        
        except Exception:
            await ctx.send("Error occured\nUsage:\n`<prefix>subtractchips <user> <amount> <chips>`")

    @commands.command(name="contactuser")
    @commands.is_owner()
    async def contactuser(self, ctx, user : discord.User = None, *words):
        try:
            if user == None or len(words) < 5:
                await ctx.send("Usage:\n`<prefix>contactuser <user> <message>`\nProvide at least 5 words to send.")
                return
            message = " ".join(words)
            await user.send(message)
            await ctx.send("Message sent!")

        except Exception:
            await ctx.send("Error occured\nUsage:\n`<prefix>contactuser <user> <message>`")
    
    @commands.command(name="updaterank")
    @commands.is_owner()
    async def updaterank(self, ctx, user : discord.User = None, *rank):
        try:
            if user == None or not rank:
                await ctx.send("Usage:\n`<prefix>updaterank <user> <rank>`")
                return
            rank = " ".join(rank)
            await self.bot.db.update_rank(user.id, rank)
            await ctx.send(f"Updated {user}'s rank to {rank.title()}.")
        except Exception:
            await ctx.send("Error occured\nUsage:\n`<prefix>updaterank <user> <rank>`")

    @commands.command(name="guilds")
    @commands.is_owner()
    async def guilds(self, ctx):
        await ctx.send(len(self.bot.guilds))


def setup(bot):
    bot.add_cog(Owner(bot))