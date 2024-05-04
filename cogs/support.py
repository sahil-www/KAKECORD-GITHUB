from settings import *

import discord
from discord.ext import commands

class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    ################################################### ERRORS #####################################################
    async def cog_command_error(self, ctx, error):
        error = getattr(error, "original", error)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You've used `<prefix>report` enough for now, please try after some time.")
            return
        else:
            await ctx.send("An unknown error occured, please report it using `<prefix>report <description>`")
            return
    ################################################################################################################
    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="support")
    @commands.guild_only()
    async def support(self, ctx):
        embed = discord.Embed(
            title="Support me",
            description="Kakecord was created to bring the world of Kakegurui to discord!  It is fairly new and there isn't a lot to do for now, but we are continuously working towards building a bigger community and adding more features, but we lack funds, if you want to see it flourish, then please do your part to support it.\n\nThese are the various ways to support the development of Kakecord.", # But a direct donation to Kakecord will be appreciated.,
            colour = 0xFF0000
        )
        embed.add_field(name="Invite Kakecord to your server", value=f"[Invite me]({BOT_INVITE})", inline=False)
        embed.add_field(name="Join the official server of Kakecord", value=f"[Join the official server]({BOT_SERVER})", inline=False)
        # embed.add_field(name="Support through donations", value=f"[]()")
        await ctx.send(embed=embed)

    # THIS COMMAND WORKS PROPERLY
    @commands.command(name="invite")
    @commands.guild_only()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Use the links below",
            colour=0xFF0000
        )
        embed.add_field(name="Invite Kakecord to your server", value=f"[Invite me]({BOT_INVITE})", inline=False)
        embed.add_field(name="Join the official server of Kakecord", value=f"[Join the official server]({BOT_SERVER})", inline=False)
        await ctx.send(embed=embed)

     # THIS COMMAND WORKS PROPERLY
    @commands.command(name="server")
    @commands.guild_only()
    async def server(self, ctx):
        await ctx.send(f"**__JOIN THE OFFICIAL SERVER__**\nJoin our server to play and chat in a Kakegurui-like environment and to participate in exciting tournaments, matches, scheduled regular games and much more!\n{BOT_SERVER}")

    @commands.command(name="report")
    @commands.guild_only()
    @commands.cooldown(rate=2, per=3600, type=commands.BucketType.user)
    async def report(self, ctx, *description):
        if len(description) < 5:
            await ctx.send("Please provide a brief description of the issue.")
            return
        description = " ".join(description)
        description += f"\nBy:\n{ctx.author}"
        report_channel = self.bot.get_channel(857608700373368863) or await self.bot.fetch_channel(857608700373368863)
        await report_channel.send(description)
        await ctx.send(f"{ctx.author.mention}, your report has been submitted, thank you for your report.")

def setup(bot):
    bot.add_cog(Support(bot))