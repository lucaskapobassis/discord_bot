import configparser

config = configparser.ConfigParser()
config.read("config.ini")

rbxInfo = config["roblox"]
discordInfo = config["bot"]

# Roblox Config
dsKey = rbxInfo["ds_key"]
dsPrefix = rbxInfo["ds_prefix"]
dsUniverse = rbxInfo["ds_universe"]
dsToken = rbxInfo["ds_token"]
# Discord Config
botToken = discordInfo["token"]
botPrefix = discordInfo["prefix"]

print(botToken)