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
        start = datetime.now()

        split_names = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        if len(split_names) == 1:

            res = find_birthday(ctx.message.content[ctx.message.content.index(words[1]):])

            embed = discord.Embed(title=res["name"],
                    description=res["info"],
                    color=0x801ecc)

            end = datetime.now()
            diff = end - start

            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

            await self.client.say("", embed = embed)

        else:
            comparison = {'west': {'value': 0, 'location': False}, 'east': {'value': 0, 'location': False}, 'north': {'value': 0, 'location': False}, 'south': {'value': 0, 'location': False}}

            embed = discord.Embed(title="Comparing Birthdates:",
                    description="remind voc to add useful stuff here later",
                    color=0x801ecc)
            for x in split_names:
                res = find_birthday(x)
                embed.add_field(name=res["name"], value=res["info"], inline=False)

                # convert date to datetime
                date = datetime.strptime(res["info"].split("(")[0].strip(), '%b %d, %Y')
                print(date)
                return

                if comparison["south"]["location"] == False:
                    comparison["south"]["value"] = res["latitude"]
                    comparison["south"]["location"] = res["name"]
                    comparison["north"]["value"] = res["latitude"]
                    comparison["north"]["location"] = res["name"]
                    comparison["west"]["value"] = res["longitude"]
                    comparison["west"]["location"] = res["name"]
                    comparison["east"]["value"] = res["longitude"]
                    comparison["east"]["location"] = res["name"]

                if res["latitude"] < comparison["south"]["value"]:
                    comparison["south"]["value"] = res["latitude"]
                    comparison["south"]["location"] = res["name"]

                if res["latitude"] > comparison["north"]["value"]:
                    comparison["north"]["value"] = res["latitude"]
                    comparison["north"]["location"] = res["name"]

                if res["longitude"] < comparison["west"]["value"]:
                    comparison["west"]["value"] = res["longitude"]
                    comparison["west"]["location"] = res["name"]

                if res["longitude"] > comparison["east"]["value"]:
                    comparison["east"]["value"] = res["longitude"]
                    comparison["east"]["location"] = res["name"]


            end = datetime.now()
            diff = end - start
            embed.description = 'Furthest **NORTH** is `{}`.\nFurthest **SOUTH** is `{}`.\nFurthest **EAST** is `{}`.\nFurthest **WEST** is `{}`.\n'.format(comparison["north"]["location"], comparison["south"]["location"], comparison["east"]["location"], comparison["west"]["location"])
            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
            await self.client.say("", embed = embed)

    @commands.command(pass_context=True)
    async def find(self, ctx):
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

    @commands.command(pass_context=True, aliases=['coords'])
    async def coordinates(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_locations = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        if len(split_locations) == 1:

            res = find_coordinates(ctx.message.content[ctx.message.content.index(words[1]):])

            embed = discord.Embed(title=res["name"],
                    description=res["info"],
                    color=0x801ecc)

            end = datetime.now()
            diff = end - start

            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

            await self.client.say("", embed = embed)

        else:
            comparison = {'west': {'value': 0, 'location': False}, 'east': {'value': 0, 'location': False}, 'north': {'value': 0, 'location': False}, 'south': {'value': 0, 'location': False}}

            embed = discord.Embed(title="Comparing Coordinates:",
                    description="remind voc to add useful stuff here later",
                    color=0x801ecc)
            for x in split_locations:
                res = find_coordinates(x)
                embed.add_field(name=res["name"], value=res["info"], inline=False)

                if comparison["south"]["location"] == False:
                    comparison["south"]["value"] = res["latitude"]
                    comparison["south"]["location"] = res["name"]
                    comparison["north"]["value"] = res["latitude"]
                    comparison["north"]["location"] = res["name"]
                    comparison["west"]["value"] = res["longitude"]
                    comparison["west"]["location"] = res["name"]
                    comparison["east"]["value"] = res["longitude"]
                    comparison["east"]["location"] = res["name"]

                if res["latitude"] < comparison["south"]["value"]:
                    comparison["south"]["value"] = res["latitude"]
                    comparison["south"]["location"] = res["name"]

                if res["latitude"] > comparison["north"]["value"]:
                    comparison["north"]["value"] = res["latitude"]
                    comparison["north"]["location"] = res["name"]

                if res["longitude"] < comparison["west"]["value"]:
                    comparison["west"]["value"] = res["longitude"]
                    comparison["west"]["location"] = res["name"]

                if res["longitude"] > comparison["east"]["value"]:
                    comparison["east"]["value"] = res["longitude"]
                    comparison["east"]["location"] = res["name"]


            end = datetime.now()
            diff = end - start
            embed.description = 'Furthest **NORTH** is `{}`.\nFurthest **SOUTH** is `{}`.\nFurthest **EAST** is `{}`.\nFurthest **WEST** is `{}`.\n'.format(comparison["north"]["location"], comparison["south"]["location"], comparison["east"]["location"], comparison["west"]["location"])
            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
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

    if len(page.cssselect("div.FSP1Dd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        information += '**{}** {}\n'.format(page.cssselect("span.cC4Myd")[i].text_content(), page.cssselect("span.A1t5ne")[i].text_content())

    return information, name

def find_birthday (msg):

    raw = get('https://www.google.com/search?q={}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("div.cC4Myd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        # identify the birthdate
        if page.cssselect("span.cC4Myd")[i].text_content().strip() == "Born:":
            information = page.cssselect("span.A1t5ne")[i].text_content()

    res = {'info': information, 'name': name}
    print(res)
    return res

def find_coordinates (msg):

    raw = get('https://en.wikipedia.org/wiki/{}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect(".longitude")) == 0:
        return "I couldn't find anything on that. Did you make a typo?", "Nothing."

    name = ''
    if len(page.cssselect(".firstHeading")) != 0:
        name = page.cssselect(".firstHeading")[0].text_content()


    information = ""
    latitude = page.cssselect(".latitude")[0].text_content()
    information += latitude
    longitude = page.cssselect(".longitude")[0].text_content()
    information += "\n" + longitude

    latitude = latitude.replace(".", "").replace("°", ".").replace("′", "").replace("″", "")
    longitude = longitude.replace(".", "").replace("°", ".").replace("′", "").replace("″", "")

    if "N" in latitude:
        latitude = float(latitude.replace("N", ""))
    else:
        latitude = float(latitude.replace("S", "")) * -1

    if "E" in longitude:
        longitude = float(longitude.replace("E", ""))
    else:
        longitude = float(longitude.replace("W", "")) * -1

    res = {'info': information, 'name': name, 'latitude': latitude, 'longitude': longitude}
    return res

def setup(client):
    client.add_cog(Google(client))
