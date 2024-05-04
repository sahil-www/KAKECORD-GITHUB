from settings import *

import discord
from discord.ext import commands

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="verify")
    async def verify(self, ctx):
        if ctx.channel.id == 860416176966598676:
            await ctx.author.add_roles(self.bot.verified_role)


def setup(bot):
    bot.add_cog(Server(bot))