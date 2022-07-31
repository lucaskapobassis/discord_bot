import configparser
from decouple import config
import datetime
import requests
import discord
import os

from discord.ext import commands

token = config("discord_token")
dskey = config("ds_key")
dsprefix = config("ds_prefix")
dsuniverse = config("ds_universe")
dstoken = config("ds_token")

groupid = config("group_id")
groupname = config("group_name")

client = commands.Bot(command_prefix = "!")
client.remove_command("help")

gamename = requests.get('https://games.roblox.com/v1/games?universeIds='+dsuniverse).json()["data"][0]["name"]

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send(f'**{(round(client.latency * 1000)/2)+0.1}ms** ping to Discord!')

@client.command()
async def membercount(ctx):
    await ctx.send(f'**{ctx.message.guild.member_count}** members!')

@client.command()
async def visits(ctx):
    visits = requests.get('https://games.roblox.com/v1/games?universeIds='+dsuniverse).json()
    em = discord.Embed(title = 'Game Visits', color = 0x0099E1)
    v2 = visits["data"][0]["visits"]
    v2 = str("{:,}".format(int(v2)))
    em.add_field(name = gamename, value = f"▶️ {v2}")
    await ctx.send(embed = em)

@client.command()
async def favs(ctx):
    favs = requests.get('https://games.roblox.com/v1/games/' + dsuniverse + '/favorites/count').json()["favoritesCount"]
    em = discord.Embed(title = 'Game Favorites', color = 0x0099E1)
    favs = str("{:,}".format(int(favs)))
    em.add_field(name = gamename, value = f"⭐ {favs}")
    await ctx.send(embed = em)

@client.command()
async def group(ctx):
    mems = requests.get('https://groups.roblox.com/v1/groups/' + groupid).json()["memberCount"]
    em = discord.Embed(title = 'Group Members', color = 0x0099E1)
    mems = str("{:,}".format(int(mems)))
    em.add_field(name = groupname, value = f"👑 {mems} Members!")
    await ctx.send(embed = em)

client.run(token)