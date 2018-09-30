import discord
from discord.ext import commands

import json
import asyncio
import time

clutch_list = []

class Clutch:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def clutch(self, ctx):
        if len(ctx.message.mentions) == 0:
            await self.client.say("You need to mention someone!")
            return

        if ctx.message.mentions[0].id in clutch_list:
            await self.client.say("They are already being voted on! Scroll above.")
            return

        if ctx.message.author.id == ctx.message.mentions[0].id:
            await self.client.say("You can't clutch yourself.")
            return

        if ctx.message.author.bot == True:
            await self.client.say("You are a bot.")
            return

        if ctx.message.mentions[0].bot == True:
            await self.client.say("You can't clutch a bot.")
            return

        clutch_list.append(ctx.message.mentions[0].id)

        embed = discord.Embed(title="Clutch Vote",
                description=f'React if you believe {ctx.message.mentions[0].mention} has clutched!\nVote within 15 seconds. At least 4 people must agree and it has to be a majority.',
                color=0x801ecc)
        msg = await self.client.say("", embed=embed)
        await self.client.add_reaction(msg, "👍")
        await self.client.add_reaction(msg, "👎")
        await asyncio.sleep(10)

        msg = await self.client.get_message(msg.channel, msg.id)
        if msg.reactions[0].count >= 2 and msg.reactions[0].count > msg.reactions[1].count:
            await self.client.say(f'Vote has been passed for {ctx.message.mentions[0].mention}!')
        else:
            await self.client.say(f'Vote for {ctx.message.mentions[0].mention} did not pass.')

        clutch_list.remove(ctx.message.mentions[0].id)

    @commands.command(pass_context=True)
    async def score(self, ctx):
        with open('data/clutch.json') as data_file:
            sets = json.load(data_file)

        if ctx.message.author.id not in list(sets):
            await self.client.say("You haven't clutched before.")
            return

        embed = discord.Embed(title="Clutch Score",
                description=f'{ctx.message.mentions[0].mention} has a clutch score of **{sets[str(ctx.message.author.id)]}**.',
                color=0x801ecc)


def clutchUp(user_id):
    # load up saved sets
    with open('data/clutch.json') as data_file:
        sets = json.load(data_file)

    # adding new dict if user isn't already there
    if str(user_id) not in list(sets):
        sets[str(user_id)] = 0

    sets[str(user_id)] += 1
    sets[str(user_id)].update(sets[str(user_id)])
    with open('data/clutch.json', 'w') as file:
        file.write(json.dumps(sets))

def setup(client):
    client.add_cog(Clutch(client))
