import configparser

config = configparser.ConfigParser()
config.read("config.ini")

rbxInfo = config["roblox"]
discordInfo = config["bot"]

dsKey = rbxInfo["ds_key"]
dsPrefix = rbxInfo["ds_prefix"]
dsUniverse = rbxInfo["ds_universe"]
dsToken = rbxInfo["ds_token"]

botToken = discordInfo["token"]

print(botToken)