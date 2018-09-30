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
            await.client.say("You need to mention someone!")
            return

        embed = discord.Embed(title="Clutch",
                description=f'React if you believe {ctx.message.mentions[0]} has clutched!\nVote within 15 seconds.',
                color=0x801ecc)
        msg = await client.say("", embed)
        await client.add_react(message, "👍")
        await client.add_react(message, "👎")
        time.sleep(15)

        print(msg.reactions)


def setup(client):
    client.add_cog(Clutch(client))
