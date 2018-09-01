from urllib.parse import urlencode, urlparse, parse_qs

from lxml.html import fromstring
from requests import get

import discord
from discord.ext import commands

from datetime import datetime

import requests
import json
import lxml


class Google:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def height(self, ctx):
        words = ctx.message.clean_content.split(" ")

        res = height(ctx.message.content[ctx.message.content.index(words[1]):], "height")

        embed = discord.Embed(title=res[1],
                description=res[0],
                color=0x801ecc)

        await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['birthday', 'born', 'age'])
    async def birth(self, ctx):
        words = ctx.message.clean_content.split(" ")

        res = age(ctx.message.content[ctx.message.content.index(words[1]):])

        embed = discord.Embed(title="something",
                description=res,
                color=0x801ecc)

        await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['google'])
    async def find(self, ctx):
        words = ctx.message.clean_content.split(" ")

        res = find(ctx.message.content[ctx.message.content.index(words[1]):])

        embed = discord.Embed(title=res[1],
                description=res[0],
                color=0x801ecc)

        await self.client.say("", embed = embed)


def height(msg, cmd):
    raw = get('https://www.google.com/search?q={} {}'.format(msg, cmd)).text
    page = fromstring(raw)

    answer = page.cssselect("div .mrH1y")[0].text_content()
    search = page.cssselect("div .PZ6wOb")[0].text_content()
    return answer, search

def age(msg):
    raw = get('https://www.google.com/search?q={}'.format(msg)).text
    page = fromstring(raw)


    birthdate = page.cssselect(".A1t5ne")[0].text_content()
    # birthplace = page.cssselect(".A1t5ne .fl")[0].text_content()
    birthplace = ""
    #print(lxml.html.tostring(page.cssselect(".A1t5ne")[0]))
    return '{}\n{}'.format(birthdate, birthplace)


def find (msg):
    raw = get('https://www.google.com/search?q={}'.format(msg)).text
    page = fromstring(raw)

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd")) - 1):
        information += '**{}** {}\n'.format(page.cssselect("span.cC4Myd")[i].text_content(), page.cssselect("span.A1t5ne")[i].text_content())

    return information, name

def setup(client):
    client.add_cog(Google(client))
