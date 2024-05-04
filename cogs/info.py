from settings import *

import discord
from discord.ext import commands

from errors.database_errors import *

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

################################################### ERRORS ########################################################
    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        # Common errors i.e. for balance and profile
        if isinstance(error, commands.UserNotFound):
            await ctx.send("The user you provided is invalid, either @mention the user or provide their ID.")
        else:
            await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")        
###################################################################################################################

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="information", aliases=["info"])
    @commands.guild_only()
    async def info(self, ctx):
        embed = discord.Embed(
            title="My Information",
            description="I am a Kakegurui-themed gambling bot.\nAlthough I am based on Kakegurui, I am not limited to it. I have all the features of a Casino but more!",
            colour = 0xFF0000
        )
        embed.set_thumbnail(url=BOT_PFP)
        latency = self.bot.latency * 1000
        latency = format(latency, ".0f")
        embed.add_field(name="Prefix", value="k!", inline=True)
        embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
        embed.add_field(name="Version", value=BOT_VERSION, inline=True)
        embed.add_field(name="Invite me to your server", value=BOT_INVITE, inline=False)
        embed.add_field(name="Join the Official Server of Kakecord", value=BOT_SERVER, inline=False)
        # embed.add_field(name="Vote me on Top.gg", value="WIP", inline=False)
        # embed.add_field(name="Donate", value="WIP", inline=False)
        await ctx.send(embed=embed)

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="ping")
    @commands.guild_only()
    async def ping(self, ctx):
        latency = self.bot.latency * 1000
        latency = format(latency, ".0f")
        await ctx.send(f"Pong! **{latency}ms.**")

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="profile", aliases=["pf"])
    @commands.guild_only()
    async def profile(self, ctx, user : discord.User = None):
        if user == None:
            user = ctx.author
        await self.bot.db.check_presence(user.id)
        status, rank, kakechips, owochips = await self.bot.db.get_info(user.id)
        embed = discord.Embed(description=status, colour=0xFF0000)
        embed.add_field(name="Rank", value=rank, inline=False)
        embed.add_field(name="Balance", value=f"**Kakechips:** {kakechips}{E_KAKECHIPS}\n**Owochips:** {owochips}{E_OWOCHIPS}", inline=False)
        embed.set_author(name=user, icon_url=user.avatar_url)
        await ctx.send(embed=embed)

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="balance", aliases=["bal", "chips"])
    @commands.guild_only()
    async def balance(self, ctx, user : discord.User = None):
        if user == None:
            user = ctx.author
        await self.bot.db.check_presence(user.id)
        kakechips, owochips = await self.bot.db.get_complete_balance(user.id)
        embed = discord.Embed(colour=0xFF0000)
        embed.add_field(name="Balance", value=f"**Kakechips:** {kakechips}{E_KAKECHIPS}\n**Owochips:** {owochips}{E_OWOCHIPS}", inline=True)
        embed.set_author(name=user, icon_url=user.avatar_url)
        await ctx.send(embed=embed)

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="status")
    @commands.guild_only()
    async def status(self, ctx, *args):
        await self.bot.db.check_presence(ctx.author.id)
        status = " ".join(args)
        status = status[:128]
        await self.bot.db.update_status(ctx.author.id, status)
        await ctx.send(f'I updated your status to "{status}"')

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="leaderboard", aliases=["lb"])
    @commands.guild_only()
    async def leaderboard(self, ctx):
        lb = await self.bot.db.get_leaderboard()
        embed = discord.Embed(
            title="Top 10 Richest Gamblers",
            colour=0xFF0000
        )
        user = self.bot.get_user(lb[0]["id"]) or await self.bot.fetch_user(lb[0]["id"])
        user_avatar = user.avatar_url
        for item, i in zip(lb, range(1, 11)):
            user = self.bot.get_user(item["id"]) or await self.bot.fetch_user(item["id"])
            embed.add_field(name=f"{i}. {user}", value=f"{item['kakechips']}{E_KAKECHIPS}", inline="False")
            print(item["id"], item["kakechips"])
        
        embed.set_thumbnail(url=user_avatar)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))