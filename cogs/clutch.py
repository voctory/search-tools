import discord
from discord.ext import commands

import json
import asyncio
import time

# load perms file
with open('data/permitted.json') as data_file:
    data = json.load(data_file)

# checks for permitted
def permitted(ctx):
    return ctx.message.author.id in data["ids"]

clutch_list = []

class Clutch:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, aliases=['c'])
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
                description=f'React if you believe {ctx.message.mentions[0].mention} has clutched!\nVote within 15 seconds. At least 3 people (besides the recipient) must agree and it has to be a majority.',
                color=0x801ecc)
        msg = await self.client.say("", embed=embed)
        await self.client.add_reaction(msg, "👍")
        await self.client.add_reaction(msg, "👎")

        # TODO: adjust to 15
        await asyncio.sleep(15)

        msg = await self.client.get_message(msg.channel, msg.id)

        # TODO: reset valeus
        usersReacted = await self.client.get_reaction_users(msg.reactions[0])
        totalReactedYes = msg.reactions[0].count

        for i in usersReacted:
            if i.id == ctx.message.mentions[0].id:
                totalReactedYes -= 1


        if totalReactedYes > 3 and msg.reactions[0].count > msg.reactions[1].count:
            await self.client.say(f'Vote has been passed for {ctx.message.mentions[0].mention}!')
            clutchUp(ctx.message.mentions[0].id, msg.reactions[0].count)
        else:
            await self.client.say(f'Vote for {ctx.message.mentions[0].mention} did not pass.')

        clutch_list.remove(ctx.message.mentions[0].id)

    @commands.command(pass_context=True)
    async def score(self, ctx):
        with open('data/clutch.json') as data_file:
            sets = json.load(data_file)

        if len(ctx.message.mentions) == 0:
            if ctx.message.author.id not in list(sets):
                await self.client.say("You haven't clutched before.")
                return

            embed = discord.Embed(title="Clutch Score",
                    description=f'{ctx.message.author.mention} has a clutch score of **{sets[str(ctx.message.author.id)]}**.',
                    color=0x801ecc)

            await self.client.say("", embed=embed)

        else:
            if ctx.message.mentions[0].id not in list(sets):
                await self.client.say("They haven't clutched before.")
                return

            embed = discord.Embed(title="Clutch Score",
                    description=f'{ctx.message.mentions[0].mention} has a clutch score of **{sets[str(ctx.message.mentions[0].id)]}**.',
                    color=0x801ecc)

            await self.client.say("", embed=embed)

    @commands.command(pass_context=True)
    @commands.check(permitted)
    async def setscore(self, ctx):
        if len(ctx.message.mentions) == 0:
            await self.client.say("You need to mention someone!")
            return

        # determining the input number
        if len(ctx.message.content.split()) != 3:
            await self.client.say("You need to specify an integer.")
            return

        if ctx.message.content.split()[2].isdigit() != True:
            await self.client.say("You need to specify an integer.")
            return

        inputNum = ctx.message.content.split()[2]
        user_id = ctx.message.mentions[0].id

        # opening clutch file
        with open('data/clutch.json') as data_file:
            sets = json.load(data_file)

        if str(user_id) not in list(sets):
            sets[str(user_id)] = 0

        sets[str(user_id)] = inputNum

        with open('data/clutch.json', 'w') as file:
            file.write(json.dumps(sets))

        await self.client.say("Successfully updated their clutch score!")

    @commands.command(pass_context=True, aliases=['lb', 'leaderboards'])
    async def leaderboard(self, ctx):
        with open('data/clutch.json') as data_file:
            sets = json.load(data_file)

        sorted_by_value = sorted(sets.items(), key=lambda kv: kv[1], reverse=True)

        current = 0
        tiebreaker = {"score": 0, "position": 0}
        lb_string = "[Click here to view the prize pool](https://www.paypal.com/pools/c/88uoO4Lcwh)\n\n"

        for i in sorted_by_value:
            if current == 10:
                break

            """
            position = current
            if tiebreaker.score == sorted_by_value[current][1]:
                position = tiebreaker.position
            """
            # TODO: Finish this

            lb_string += f'**{current + 1}.** <@{sorted_by_value[current][0]}> ({sorted_by_value[current][1]} points)\n'
            current += 1

        embed = discord.Embed(title="Clutch Leaderboard",
                description=lb_string,
                color=0x801ecc)

        await self.client.say("", embed=embed)

def clutchUp(user_id, count):
    # load up saved sets
    with open('data/clutch.json') as data_file:
        sets = json.load(data_file)

    # adding new dict if user isn't already there
    if str(user_id) not in list(sets):
        sets[str(user_id)] = 0

    sets[str(user_id)] += 1

    if count > 6:
        sets[str(user_id)] += 1

    if count > 9:
        sets[str(user_id)] += 1

    if count > 12:
        sets[str(user_id)] += 2

    with open('data/clutch.json', 'w') as file:
        file.write(json.dumps(sets))

def setup(client):
    client.add_cog(Clutch(client))
