import configparser
from decouple import config
import datetime
import discord
import os

from discord.ext import commands

token = config("discord_token")
dskey = config("ds_key")
dsprefix = config("ds_prefix")
dsuniverse = config("ds_universe")
dstoken = config("ds_token")

client = commands.Bot(command_prefix = "!")
client.remove_command("help")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send(f'**{(round(client.latency * 1000)/2)+0.1}ms** ping to Discord!')

@client.command()
async def membercount(ctx):
    await ctx.send(f'**{ctx.message.guild.member_count}** members!')

client.run(token)