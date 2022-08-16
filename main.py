from decouple import config
import datetime
import requests
import discord
import os

from discord.ext import commands
from discord.ext.commands import cooldown

token = config("discord_token")
dskey = config("ds_key")
dsprefix = config("ds_prefix")
dsuniverse = config("ds_universe")
dstoken = config("ds_token")
groupid = config("group_id")
groupname = config("group_name")
test_enabled = config("test_enabled", "False") == "True"

if test_enabled == True:
    token = config("test_token")

client = commands.Bot(command_prefix = "!", activity = discord.Game(name="!help"))
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
async def invite(ctx):
    em = discord.Embed(title = 'Click to invite!', url = "https://digging.games/bot", color = 0x0099E1, description = "Click above to invite the bot to your own server!")
    await ctx.send(embed = em)

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

baseUrl = 'https://apis.roblox.com/datastores/v1/universes/'
objectsUrl = baseUrl+dsuniverse+'/standard-datastores/datastore/entries/entry'
listObjectsUrl = baseUrl+dsuniverse+'/standard-datastores/datastore/entries'
def getData(userId: str):
    playerToGet = dsprefix+str(userId)
    payload = {'datastoreName': dskey, 'entryKey': playerToGet}
    r = requests.get('https://apis.roblox.com/datastores/v1/universes/'+dsuniverse+'/standard-datastores/datastore/entries/entry', params=payload, headers={'x-api-key': dstoken}).json()
    return r

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['','k','m','b','t','qd','qn','sx','sp','o','n','d','ud','dd', 'td', 'qtd', 'qnd', 'sxd', 'spd', 'od', 'nd', 'vg', 'uvg', 'dvg', 'tvg', 'qtvg', 'qnvg', 'sxvg', 'spvg', 'ovg', 'nvg', 'tt', 'utt', 'dtt', 'g', 'ttn', 'qttn', 'qntn', 'sxtn', 'sptn','otn','ntn','cn'][magnitude])

@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def profile(ctx, user: str):
    try:
        userId = 0
        userName = 'Player'

        try:
            userId =  requests.get(f'https://api.roblox.com/users/get-by-username?username={user}').json()["Id"]
        except:
            em = discord.Embed(title = 'Error', description = 'That user does not exist!', color = 0xED4245)
            await ctx.reply(embed = em)
            return

        try:
            userName =  requests.get(f'https://users.roblox.com/v1/users/{userId}').json()["name"]
        except:
            em = discord.Embed(title = 'Error', description = 'Something went wrong on our end!', color = 0xED4245)
            await ctx.reply(embed = em)
            return

        userData = {}
        try:
            userData = getData(userId)
        except:
            em = discord.Embed(title = 'Error', description = 'That user hasnt played!', color = 0xED4245)
            await ctx.reply(embed = em)
            return

        playerData = userData["Data"]
        
        em = discord.Embed(title = f'{userName}', description = 'Player Statistics', color = 0x0099E1, url = "https://www.roblox.com/users/"+str(userId)+"/profile")

        brokenCount = playerData["BoardStats"]["Fireworks Broken"]
        brokenCount = human_format(brokenCount)
        em.add_field(name = "Fireworks", value = f"{brokenCount}", inline=True)
        eggCount = playerData["BoardStats"]["Eggs Hatched"]
        eggCount = human_format(eggCount)
        em.add_field(name = "Eggs", value = f"{eggCount}", inline=True)
        timePlayed = playerData["BoardStats"]["Time Played"]
        timePlayed = datetime.timedelta(seconds=timePlayed)
        em.add_field(name = "Time Played", value = f"{timePlayed}", inline=True)
        techCoins = playerData["BoardStats"]["Total Tech Coins"] or 0
        techCoins = human_format(techCoins)
        em.add_field(name = "Total Tech Coins", value = f"{techCoins}", inline=False)
        totalCoins = playerData["BoardStats"]["Total Coins"]
        totalCoins = human_format(totalCoins)
        em.add_field(name = "Total Coins", value = f"{totalCoins}", inline=False)
        totalGems = playerData["BoardStats"]["Total Gems"]
        totalGems = human_format(totalGems)
        em.add_field(name = "Total Gems", value = f"{totalGems}", inline=True)
        em.set_footer(text=f"UserId: {str(userId)}")
    
        headshot = "https://www.roblox.com/headshot-thumbnail/image?userId=" + str(userId) + "&width=420&height=420&format=png"
        em.set_thumbnail(url = headshot)

        await ctx.reply(embed = em)
    except:
        em = discord.Embed(title = 'Error', description = 'That user hasnt played!', color = 0xED4245)
        await ctx.reply(embed = em)
        return

# Catch Errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): # or discord.ext.commands.errors.CommandNotFound as you wrote
        em = discord.Embed(title = 'Slow it down!', description = f'Try again in {round(error.retry_after, 1)} seconds!', color = 0xED4245)
        await ctx.reply(embed = em)
        return

    if isinstance(error, commands.CommandNotFound): # or discord.ext.commands.errors.CommandNotFound as you wrote
        em = discord.Embed(title = 'Error', description = 'Unknown command!', color = 0xED4245)
        await ctx.reply(embed = em)

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = 'Bot Commands', description = 'Here are some commands you can use:', color = 0x0099E1)
    em.add_field(name = "Games", value = "!visits, !favs, !group, !profile [username]")#, !claim [code]")
    em.add_field(name = "Bot Stuff", value = "!ping, !membercount !invite")
    await ctx.send(embed = em)

client.run(token)