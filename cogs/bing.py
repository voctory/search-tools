from urllib.parse import urlencode, urlparse, parse_qs

from lxml.html import fromstring
from requests import get

import discord
from discord.ext import commands

from datetime import datetime
from dateutil import relativedelta

import requests
import json
import lxml


class Google:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def b(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        res = find(ctx.message.content[ctx.message.content.index(words[1]):])

        embed = discord.Embed(title=res[1],
                description=res[0],
                color=0x801ecc)

        end = datetime.now()
        diff = end - start

        embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

        await self.client.say("", embed = embed)


def find (msg):

    raw = get('https://www.bing.com/search?q={}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect(".b_focusTextMedium")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect(".b_focusLabel")[0].text_content()
    information = page.cssselect(".b_focusTextMedium")[0].text_content()

    return information, name


def setup(client):
    client.add_cog(Google(client))
