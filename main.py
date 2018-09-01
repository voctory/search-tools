import discord
from discord.ext import commands

import asyncio
import json

# load config file
with open('config.json') as data_file:
    data = json.load(data_file)

# set prefix
client = commands.Bot(command_prefix = data["prefix"])

# load cogs
extensions = ['cogs.genius',
            'cogs.google',
            'cogs.error_handler']

# checks for owner perms
def ownerPerms(ctx):
    return ctx.message.author.id in data["owners"]

# triggered when bot is logged in
@client.event
async def on_ready():
    print('Bot online.')

# load cogs command
@client.command()
@commands.check(ownerPerms)
async def load(extension):
    try:
        client.load_extension('cogs.{}'.format(extension))
        print('Loaded {}'.format(extension))
        await client.say('Loaded `{}`.'.format(extension))
    except Exception as error:
        print('{} cannot be loaded. [{}]'.format(extension, error))
        await client.say('`{}` cannot be loaded. [{}]'.format(extension, error))

# unload cogs command
@client.command()
@commands.check(ownerPerms)
async def unload(extension):
    try:
        client.unload_extension('cogs.{}'.format(extension))
        print('Unloaded {}'.format(extension))
        await client.say('Unloaded {}.'.format(extension))
    except Exception as error:
        print('`{}` cannot be unloaded. [{}]'.format(extension, error))
        await client.say('`{}` cannot be unloaded. [{}]'.format(extension, error))

# reload cogs command
@client.command()
@commands.check(ownerPerms)
async def reload(extension):
    try:
        client.unload_extension('cogs.{}'.format(extension))
        client.load_extension('cogs.{}'.format(extension))
        print('Reloaded {}'.format(extension))
        await client.say('Reloaded `{}`.'.format(extension))
    except Exception as error:
        print('{} cannot be reloaded. [{}]'.format(extension, error))
        await client.say('`{}` cannot be reloaded. [{}]'.format(extension, error))

# something to do with cogs
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(extension, error))

# login
client.run(data["discord"])
