# 20-05-2021
# from discord.ext.commands.errors import CommandNotFound, NoPrivateMessage, NotOwner
from settings import *

import sys
# This sys contains a list of paths where the intrepreter will look for the required module
sys.path.append(f"{ROOT_DIR}")

import asyncpg
from databasehelper import DatabaseHelper

from discord.ext import commands
import discord

###############################################################################################################

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("k."), case_insensitive=True, description="Prefix = k.\nKakeguru-themed gambling bot.\nA kakegurui-themed gambling bot.\nAlthough Kakecord is based on Kakegurui, It's not limited to it. It has all the features of a Casino but more!\nWe currently lack funds, and it's very hard for us to keep the bot running without support, so if you like Kakecord, then please consider supporting it through donations.",
    strip_after_prefix=True, activity=discord.Game("k.help"), intents=intents
)
bot.remove_command("help")

logs_joins = None
logs_leaves = None

@bot.event
async def on_ready():
    # Official guild
    official_guild = bot.get_guild(806764640464928789)
    bot.verified_role = official_guild.get_role(806842633682812950)
    bot.server_booster_role = official_guild.get_role(852802620468363295)

    # Logging
    global logs_joins, logs_leaves
    logs_ready = bot.get_channel(861105042823577643)
    logs_joins = bot.get_channel(861105073169367080)
    logs_leaves = bot.get_channel(861105087169167361)

    await logs_ready.send('I am on')
    print("Bot is ready")

@bot.event
async def on_guild_join(guild):
    embed = discord.Embed(
        title = "Server Joined",
        description = f"{guild.name}\n{guild.id}",
        colour = 0XFF0000
    )
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(name="Owner", value=f"{guild.owner}\n{guild.owner.id}")
    embed.add_field(name="Created", value=guild.created_at)
    embed.set_footer(text=f"Now in {len(bot.guilds)} servers.")
    await logs_joins.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    embed = discord.Embed(
        title = "Server Left",
        description = f"{guild.name}\n{guild.id}",
        colour = 0XFF0000
    )
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Member Count", value=guild.member_count)
    embed.add_field(name="Owner", value=f"{guild.owner}\n{guild.owner.id}")
    embed.add_field(name="Created", value=guild.created_at)
    embed.set_footer(text=f"Now in {len(bot.guilds)} servers.")
    await logs_leaves.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    pass

db = None
async def create_db_pool():
    global db
    db = await asyncpg.create_pool(dsn=H_URL,
    database = H_DATABASE,
    user = H_USER,
    password = H_PASS
    )
    print("DB ready")
    
bot.loop.run_until_complete(create_db_pool())
bot.db = DatabaseHelper(db)

bot.load_extension(f"cogs.help")
bot.load_extension(f"cogs.info")
bot.load_extension(f"cogs.economy")
bot.load_extension(f"cogs.gamble")
bot.load_extension(f"cogs.support")
bot.load_extension(f"cogs.owner")
bot.load_extension(f"cogs.server")


# Run the bot
bot.run(BOT_TOKEN)