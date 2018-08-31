from urllib.parse import urlencode, urlparse, parse_qs

from lxml.html import fromstring
from requests import get

import discord
from discord.ext import commands

from datetime import datetime

import requests
import json


class Google:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def height(self, ctx):
        words = ctx.message.clean_content.split(" ")

        answer = find(ctx.message.content[ctx.message.content.index(words[1]):], "height")

        embed = discord.Embed(title='hello',
                description=answer,
                color=0x801ecc)

        await self.client.say("", embed = embed)

def find(msg, cmd):
    raw = get('https://www.google.com/search?q={} {}'.format(msg, cmd)).text
    page = fromstring(raw)

    answer = page.cssselect("div .mrH1y")[0].text_content()
    return answer

def setup(client):
    client.add_cog(Google(client))
