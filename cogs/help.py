import asyncio
from discord import colour
from discord.embeds import EmptyEmbed
from settings import *

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    ################################################# HELP GROUP ##################################################

    @commands.group(name="help", case_insensitive=True, invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="List of commands",
            description="Use `<prefix>help <command>` to get more information on a particular command",
            colour = 0xFF0000
        )
        embed.add_field(name=f"{E_INFO} Information", value="`information`, `ping`, `leaderboard`, `status`, `profile`, `balance`, `privacypolicy`", inline=False)
        # `balance`, `give`, `info`, `invite`, `ping`, `profile`, `server`, `status`, `support`", inline=False)
        embed.add_field(name=f"{E_CHIPS} Chips/Economy", value="`give`, `work`", inline=False)
        embed.add_field(name=f"{E_GAMBLING} Gambling", value="`games`, `instructions`, `challenge`, `botchallenge`", inline=False)
        embed.add_field(name=f"{E_SUPPORT} Support", value="`support`, `invite`, `server`, `report`", inline=False)
        embed.add_field(name=f"{E_QUESTION} More Information", value=f"[Read Kakecord ToS and Privacy Policy](https://pastebin.com/RdULsWUF)\n[FAQ](https://pastebin.com/fWsW2Ca8)\n[Still need help? Ask your questions here]({BOT_SERVER})", inline=False)
        embed.set_footer(text="Please consider supporting Kakecord using `<prefix>support`")
        await ctx.send(embed=embed)
        
    ################################################## ERRORS #####################################################

    ###############################################################################################################    
    @help.command(name="information", aliases=["info"])
    async def help_info(self, ctx):
        embed = discord.Embed(
            title="<prefix>information",
            description="Get detailed information about the bot.",
            colour=0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>information`")
        embed.add_field(name="Alias", value="`info`")
        await ctx.send(embed=embed)

    @help.command(name="ping")
    async def help_ping(self, ctx):
        embed = discord.Embed(
            title="<prefix>ping",
            description="Get bot latency.",
            colour=0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>ping`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)

    @help.command(name="leaderboard", aliases=["lb"])
    async def help_leaderboard(self, ctx)   :
        embed = discord.Embed(
            title = "<prefix>leaderboard",
            description = "View the top 10 richest gamblers on Kakecord.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>leaderboard`")
        embed.add_field(name="Alias", value="lb")
        await ctx.send(embed=embed)

    @help.command(name="status")
    async def help_status(self, ctx):
        embed = discord.Embed(
            title="<prefix>status",
            description="Customize your status.\n> Your status will appear in your profile.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>status <status>`")
        embed.add_field(name="Alias", value="None")
        embed.set_footer(text="Maximum length of status is 128 characters.")
        await ctx.send(embed=embed)

    @help.command(name="profile", aliases=["pf"])
    async def help_profile(self, ctx):
        embed = discord.Embed(
            title="<prefix>profile",
            description="View anyone's profile.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>profile | <user>`")
        embed.add_field(name="Alias", value="`pf`")
        embed.set_footer(text="The arguments after `|` are optional.")
        await ctx.send(embed=embed)

    @help.command(name="balance", aliases=["bal", "chips"])
    async def help_balance(self, ctx):
        embed = discord.Embed(
            title="<prefix>balance",
            description="View anyone's balance.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>balance <user>`")
        embed.add_field(name="Alias", value="`bal`, `chips`")
        embed.set_footer(text="The arguments after `|` are optional.")
        await ctx.send(embed=embed)

    @commands.command(name="privacypolicy")
    async def privacypolicy(self, ctx):
        embed = discord.Embed(
            title = "Privacy Policy",
            descrption = f"The only data Kakecord collects:\n1. All the servers Kakecord is going into and the name and the amount of members in that server. And we do so only to see the statistics of Kakecord.\n 2. Your name is displayed on the leaderboard wherever and whenever the leaderboard command is used, when you are among the top 10 riches gamblers.\n**Kakecord respects your privacy and doesn't sell this data anywhere.\nIf you have questions, then feel free to ask in", #[Kakecord's official server]({BOT_SERVER})"
            colour = 0xFF0000
        )
        await ctx.send(embed=embed)
    
    @help.command(name="privacypolicy")
    async def help_privacy_policy(self, ctx):
        embed = discord.Embed(
            title="<prefix>privacypolicy",
            description="View the privacy policy of Kakecord.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>privacypolicy`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)

    @help.command(name="give")
    async def help_give(self, ctx):
        embed = discord.Embed(
            title="<prefix>give",
            description="Give your chips to anyone else.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>give <user> <amount> <chips>`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)
    
    @help.command(name="work")
    async def help_work(self, ctx):
        embed = discord.Embed(
            title = "<prefix>work",
            description = f"Earn kakechips{E_KAKECHIPS} by using this command.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>work`")
        embed.add_field(name="Alias", value="None")
        embed.add_field(name="Cooldown", value="1 hour")
        await ctx.send(embed=embed)
    
    @help.command(name="games", aliases=["game", "gambling", "gamble"])
    async def help_games(self, ctx):
        embed = discord.Embed(
            title="<prefix>games",
            description="View the list of available games for a particular category.\nAvailable categories:\n> challenge\n> botchallenge",
            colour=0XFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>games <category>`")
        embed.add_field(name="Alias", value="`game`, `gambling`, `gambles`")
        await ctx.send(embed=embed)

    @help.command(name="instructions", aliases=["instruction", "ins", "rule", "rules"])
    async def help_instructions(self, ctx):
        embed = discord.Embed(
            title="<prefix>instructions",
            description="View the instructions on how to play a particular game.\nAvailable games:\n> rockpaperscissors\n> tictactoe\n> coinflip",
            colour=0XFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>instructions <game>`")
        embed.add_field(name="Alias", value="`instruction`, `ins`, `rules`, `rule`, `help`")
        await ctx.send(embed=embed)

    @help.command(name="challenge", aliases=["ch", "challenges"])
    async def help_challenge(self, ctx):
        embed = discord.Embed(
            title = "<prefix>challenge",
            description = "Challenge a player to a game.\n> Get the list of available games using `<prefix>games challenge`",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>challenge <game> <user> | <bet> <chips>`")
        embed.add_field(name="Alias", value="`ch`")
        embed.set_footer(text="The arguments after `|` are optional.")
        await ctx.send(embed=embed)

    @help.command(name="botchallenge", aliases=["bch", "botchallenges"])
    async def help_botchallenge(self, ctx):
        embed = discord.Embed(
            title = "<prefix>botchallenge",
            description = "Challenge me to a game.\n> Get the list of available games using `<prefix>games botchallenge`",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>botchallenge <game> <bet> <chips>`")
        embed.add_field(name="Alias", value="`ch`")
        embed.set_footer(text=f"You can't bet owochips against me.")
        await ctx.send(embed=embed)
    
    @help.command(name="support")
    async def help_support(self, ctx):
        embed = discord.Embed(
            title="<prefix>support",
            description="Get the various ways to support Kakecord.",
            colour=0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>support`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)
    
    @help.command(name="invite")
    async def help_invite(self, ctx):
        embed = discord.Embed(
            title="<prefix>invite",
            description="Get the bot and server invitation links.",
            colour=0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>invite`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)
    
    @help.command(name="server")
    async def help_server(self, ctx):
        embed = discord.Embed(
            title="<prefix>server",
            description="Get the invitation link to the official server of Kakecord.",
            colour=0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>server`")
        embed.add_field(name="Alias", value="None")
        await ctx.send(embed=embed)

    @help.command(name="report")
    async def help_report(self, ctx):
        embed = discord.Embed(
            title = "<prefix>report",
            description = "Report something to the moderators of the bot.\n> Everything after `<prefix>report` will be sent to the moderators of the bot, so describe the issue briefly.",
            colour = 0xFF0000
        )
        embed.add_field(name="Usage", value="`<prefix>report <description>`")
        embed.add_field(name="Alias", value="None")
        embed.set_footer(text="If there is a bug/error in a command, please report it immediately using this command.")
        await ctx.send(embed=embed)

    ############################################ INSTRUCTIONS COPY #################################################
    
    @help.command(name="rockpaperscissors", aliases=["rockpaperscissor", "rps"])
    async def help_rockpaperscissors(self, ctx):
        embed = discord.Embed(
            title = "Rock Paper Scissors",
            description = (
                """__**Basics:**__
                __The objective of the game is to beat your opponent's hand with your hand.__
                Rock beats Paper
                Paper beats Scissors
                Scissors beat Rock
                
                __**Instructions**__**
                For `<prefix>challenge`:**
                A direct message will be sent to both players, each player can choose their hand by simply reacting to that message.
                
                For **`<prefix>botchallenge`:**
                A message will be posted in the channel where the game was called, the player can choose their hand by reacting to that message."""
            ),
            colour = 0xFF0000
        )
        embed.set_footer(text="Failure to react on time will result in the cancellation of the game and the bets will be returned.")
        embed.set_thumbnail(url=I_RPS)
        await ctx.send(embed=embed)

    @help.command(name="tictactoe", aliases=["ttt"])
    async def help_tictactoe(self, ctx):
        embed = discord.Embed(
            title = "Tic Tac Toe",
            description = (
                """__**Basics:**__
                __The objective of the game is to make a straight-sequence of 3 (of your respective symbol) on the board.__
                
                __**Instructions**__
                **For `<prefix>challenge`:**
                The board will be sent in a format where every empty box will represent a letter (namely: a, b, c, d, e, f, g, h, i).
                Both of the players, on their respective turns, will have to reply with the letter of the box which they want to mark with their symbol, the boxes that have already been marked can't be marked again.
                
                **For `<prefix>botchallenge`:**
                Unavailable."""
            ),
            colour = 0xFF0000
        )
        embed.set_footer(text="Failure to repond on time will result in the player's defeat and the bet will not be returned.")
        embed.set_thumbnail(url=I_TTT)
        await ctx.send(embed=embed)

    @help.command(name="coinflip", aliases=["cf"])
    async def help_coinflip(self, ctx):
        embed = discord.Embed(
            title = "Coin Flip",
            description =(
                """__**Basics**__
                A coin will be flipped and the side will determine the winner."""
            ),
            colour = 0xFF0000
        )
        embed.set_thumbnail(url=I_COINFLIP)
        await ctx.send(embed=embed)

    @help.command(name="blackjack", aliases=["bj"])
    async def help_blackjack(self, ctx):
        embed = discord.Embed(
            title = "Blackjack",
            description = (
                """__**Basics:**__
                [Learn the basics of blackjack here](https://bicyclecards.com/how-to-play/blackjack/)
                
                __**Instructions**__
                **For `<prefix>challenge`:**
                Unavailable
                
                **For `<prefix>botchallenge`:**
                Reply with `hit`, `stand` or `doubledown` to take the corresponding action."""
            ),
            colour = 0xFF0000
        )
        embed.set_footer(text="Failure to respond on time will get you to stand from the game automatically.")
        embed.set_thumbnail(url=I_BJ)
        await ctx.send(embed=embed)

    @help.command(name="russianroulette", aliases=["rr"])
    async def help_russianroulette(self, ctx):
        embed = discord.Embed(
            title = "Russian Roulette",
            description = (
                """__**Basics:**__
                __The objective of the game is to survive.__
                A revolver will be loaded with a single bullet and every player will have to pull the trigger one by one.
                The game will go on until the bullet goes off (i.e. the other player dies)."""
            ),
            colour = 0xFF0000
        )
        embed.set_thumbnail(url=I_REVOLVER)
        await ctx.send(embed=embed)
        
    # async def donate(self, ctx):
    # self.help = self.bot.get_cog("Help")


def setup(bot):
    bot.add_cog(Help(bot))