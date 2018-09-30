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

import asyncio
from threading import Thread

from google_images_download import google_images_download


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

        comparison = {'youngest': {'value': 0, 'name': False}, 'oldest': {'value': 0, 'name': False}}

        embed = discord.Embed(title="Comparing Birthdates:",
                description="remind voc to add useful stuff here later",
                color=0x801ecc)

        if len(split_names) == 1:
            results = [{}]
        else:
            results = [{} for x in split_names]

        threads = []
        for ii in range(len(split_names)):
            # We start one thread per url present.
            process = Thread(target=find_birthday, args=[split_names[ii], results, ii])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        for x in results:
            res = x
            embed.add_field(name=res["name"], value=res["info"], inline=False)

            # convert date to datetime
            released = res["info"].split("(")[0].strip().replace(",", "", 1).split(",")[0]
            date = ''
            try:
                date = datetime.strptime(released, '%B %d %Y').date()
            except:
                try:
                    date = datetime.strptime(released, '%Y').date()
                except:
                    date = datetime.strptime(released, '%B %Y').date()

            if comparison["youngest"]["name"] == False:
                comparison["youngest"]["name"] = res["name"]
                comparison["youngest"]["value"] = date
                comparison["oldest"]["name"] = res["name"]
                comparison["oldest"]["value"] = date

            if date > comparison["youngest"]["value"]:
                comparison["youngest"]["value"] = date
                comparison["youngest"]["name"] = res["name"]

            if date < comparison["oldest"]["value"]:
                comparison["oldest"]["value"] = date
                comparison["oldest"]["name"] = res["name"]


        end = datetime.now()
        diff = end - start
        embed.description = '**YOUNGEST** is `{}`.\n**OLDEST** is `{}`.'.format(comparison["youngest"]["name"], comparison["oldest"]["name"])
        embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
        await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['pub', 'publish'])
    async def published(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_names = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        if len(split_names) == 1:

            res = find_published(split_names[0])
            print(res)

            embed = discord.Embed(title=res["name"],
                    description=res["info"],
                    color=0x801ecc)

            end = datetime.now()
            diff = end - start

            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

            await self.client.say("", embed = embed)

        else:
            comparison = {'youngest': {'value': 0, 'name': False}, 'oldest': {'value': 0, 'name': False}}

            embed = discord.Embed(title="Comparing Publish Date:",
                    description="remind voc to add useful stuff here later",
                    color=0x801ecc)
            for x in split_names:
                res = find_published(x)
                embed.add_field(name=res["name"], value=res["info"], inline=False)

                # convert date to datetime
                released = res["info"].split("(")[0].strip().replace(",", "", 1).split(",")[0]
                date = ''
                try:
                    date = datetime.strptime(released, '%B %d %Y').date()
                except:
                    try:
                        date = datetime.strptime(released, '%Y').date()
                    except:
                        date = datetime.strptime(released, '%B %Y').date()

                if comparison["youngest"]["name"] == False:
                    comparison["youngest"]["name"] = res["name"]
                    comparison["youngest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]
                    comparison["oldest"]["value"] = date

                if date > comparison["youngest"]["value"]:
                    comparison["youngest"]["value"] = date
                    comparison["youngest"]["name"] = res["name"]

                if date < comparison["oldest"]["value"]:
                    comparison["oldest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]


            end = datetime.now()
            diff = end - start
            embed.description = '**LATEST PUBLISHED** is `{}`.\n**EARLIEST PUBLISHED** is `{}`.'.format(comparison["youngest"]["name"], comparison["oldest"]["name"])
            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
            await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['rel', 'release'])
    async def released(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_names = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        if len(split_names) == 1:

            res = find_release(split_names[0])
            print(res)

            embed = discord.Embed(title=res["name"],
                    description=res["info"],
                    color=0x801ecc)

            end = datetime.now()
            diff = end - start

            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

            await self.client.say("", embed = embed)

        else:
            comparison = {'youngest': {'value': 0, 'name': False}, 'oldest': {'value': 0, 'name': False}}

            embed = discord.Embed(title="Comparing Release Date:",
                    description="remind voc to add useful stuff here later",
                    color=0x801ecc)
            for x in split_names:
                res = find_release(x)
                embed.add_field(name=res["name"], value=res["info"], inline=False)

                # convert date to datetime
                released = res["info"].split("(")[0].strip().replace(",", "", 1).split(",")[0]
                date = ''
                try:
                    date = datetime.strptime(released, '%B %d %Y').date()
                except:
                    try:
                        date = datetime.strptime(released, '%Y').date()
                    except:
                        date = datetime.strptime(released, '%B %Y').date()

                if comparison["youngest"]["name"] == False:
                    comparison["youngest"]["name"] = res["name"]
                    comparison["youngest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]
                    comparison["oldest"]["value"] = date

                if date > comparison["youngest"]["value"]:
                    comparison["youngest"]["value"] = date
                    comparison["youngest"]["name"] = res["name"]

                if date < comparison["oldest"]["value"]:
                    comparison["oldest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]


            end = datetime.now()
            diff = end - start
            embed.description = '**LATEST RELEASED** is `{}`.\n**EARLIEST RELEASED** is `{}`.'.format(comparison["youngest"]["name"], comparison["oldest"]["name"])
            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
            await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['fil', 'movie'])
    async def film(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_names = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        if len(split_names) == 1:

            res = film_release(split_names[0])
            print(res)

            embed = discord.Embed(title=res["name"],
                    description=res["info"],
                    color=0x801ecc)

            end = datetime.now()
            diff = end - start

            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

            await self.client.say("", embed = embed)

        else:
            comparison = {'youngest': {'value': 0, 'name': False}, 'oldest': {'value': 0, 'name': False}}

            embed = discord.Embed(title="Comparing Release Date:",
                    description="remind voc to add useful stuff here later",
                    color=0x801ecc)
            for x in split_names:
                res = film_release(x)
                embed.add_field(name=res["name"], value=res["info"], inline=False)

                # convert date to datetime
                released = res["info"].split("(")[0].strip().replace(",", "", 1).split(",")[0]
                date = ''
                try:
                    date = datetime.strptime(released, '%B %d %Y').date()
                except:
                    try:
                        date = datetime.strptime(released, '%Y').date()
                    except:
                        date = datetime.strptime(released, '%B %Y').date()

                if comparison["youngest"]["name"] == False:
                    comparison["youngest"]["name"] = res["name"]
                    comparison["youngest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]
                    comparison["oldest"]["value"] = date

                if date > comparison["youngest"]["value"]:
                    comparison["youngest"]["value"] = date
                    comparison["youngest"]["name"] = res["name"]

                if date < comparison["oldest"]["value"]:
                    comparison["oldest"]["value"] = date
                    comparison["oldest"]["name"] = res["name"]


            end = datetime.now()
            diff = end - start
            embed.description = '**LATEST RELEASED** is `{}`.\n**EARLIEST RELEASED** is `{}`.'.format(comparison["youngest"]["name"], comparison["oldest"]["name"])
            embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))
            await self.client.say("", embed = embed)

    @commands.command(pass_context=True)
    async def find(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_names = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")

        embed = discord.Embed(title="Find Command",
                color=0x801ecc)

        if len(split_names) == 1:
            results = [{}]
        else:
            results = [{} for x in split_names]

        threads = []
        for ii in range(len(split_names)):
            # We start one thread per url present.
            process = Thread(target=find, args=[split_names[ii], results, ii])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        for x in results:
            res = x
            embed.add_field(name=res["name"], value=res["info"], inline=False)

        end = datetime.now()
        diff = end - start

        embed.set_footer(text='Took {} milliseconds to process.'.format(round((diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000))))

        await self.client.say("", embed = embed)

    @commands.command(pass_context=True, aliases=['coords', 'cd', 'cds'])
    async def coordinates(self, ctx):
        words = ctx.message.clean_content.split(" ")
        start = datetime.now()

        split_locations = ctx.message.clean_content[ctx.message.clean_content.index(words[1]):].split(",")
        comparison = {'west': {'value': 0, 'location': False}, 'east': {'value': 0, 'location': False}, 'north': {'value': 0, 'location': False}, 'south': {'value': 0, 'location': False}}

        embed = discord.Embed(title="Comparing Coordinates:",
                description="remind voc to add useful stuff here later",
                color=0x801ecc)

        if len(split_locations) == 1:
            results = [{}]
        else:
            results = [{} for x in split_locations]

        threads = []
        for ii in range(len(split_locations)):
            # We start one thread per url present.
            process = Thread(target=find_coordinates, args=[split_locations[ii], results, ii])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        for x in results:
            res = x
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


def find (msg, result, index):

    raw = get('https://www.google.com/search?q={}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("div.FSP1Dd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        information += '**{}** {}\n'.format(page.cssselect("span.cC4Myd")[i].text_content(), page.cssselect("span.A1t5ne")[i].text_content())

    result[index] = {'info': information, 'name': name}
    return True

def find_birthday_alt (msg, result, index):

    raw = get('https://www.google.com/search?q={}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("span.cC4Myd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        # identify the birthdate
        if page.cssselect("span.cC4Myd")[i].text_content().strip() == "Born:":
            information = page.cssselect("span.A1t5ne")[i].text_content()

    result[index] = {'info': information, 'name': name}
    return True

def find_birthday (msg, result, index):

    raw = get('https://en.wikipedia.org/wiki/{}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect(".bday")) == 0:
        # TODO: fix this
        # return "I couldn't find anything on that. Did you make a typo?", "Nothing."

        return find_birthday_alt(msg, result, index)

    name = page.cssselect(".firstHeading")[0].text_content()

    date = datetime.strptime(page.cssselect(".bday")[0].text_content(), '%Y-%m-%d')
    information = datetime.strftime(date, '%B %d, %Y')
    information += " (age {} years)".format(relativedelta.relativedelta(datetime.now().date(), date.date()).years)

    result[index] = {'info': information, 'name': name}
    return True

def find_published (msg):

    raw = get('https://www.google.com/search?q={} publication date'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("span.cC4Myd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        # identify the birthdate
        if page.cssselect("span.cC4Myd")[i].text_content().strip() == "Originally published:":
            information = page.cssselect("span.A1t5ne")[i].text_content()

    res = {'info': information, 'name': name}
    return res

def find_release (msg):

    raw = get('https://www.google.com/search?q={} release date'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("span.cC4Myd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        # identify the birthdate
        if page.cssselect("span.cC4Myd")[i].text_content().strip() == "Release date:":
            information = page.cssselect("span.A1t5ne")[i].text_content()

    res = {'info': information, 'name': name}
    return res

def film_release (msg):

    raw = get('https://en.wikipedia.org/wiki/{} (film)'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect(".bday")) == 0:
        # TODO: fix this
        # return "I couldn't find anything on that. Did you make a typo?", "Nothing."

        return film_release_alt(msg)

    name = page.cssselect(".firstHeading")[0].text_content()

    date = datetime.strptime(page.cssselect(".bday")[0].text_content(), '%Y-%m-%d')
    information = datetime.strftime(date, '%B %d, %Y')
    information += " (age {} years)".format(relativedelta.relativedelta(datetime.now().date(), date.date()).years)

    res = {'info': information, 'name': name}
    return res

def film_release_alt (msg):

    raw = get('https://www.google.com/search?q={} release date'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect("span.cC4Myd")) == 0:
        return "I couldn't find anything on that. Maybe specifying if it's a film or movie would help?", "Nothing."

    name = page.cssselect("div.FSP1Dd")[0].text_content()

    information = ""
    for i in range(0, len(page.cssselect(".cC4Myd"))):
        # identify the birthdate
        if page.cssselect("span.cC4Myd")[i].text_content().strip() == "Release date:":
            information = page.cssselect("span.A1t5ne")[i].text_content()

    res = {'info': information, 'name': name}
    return res

def find_coordinates_alt (msg, result, index):

    raw = get('https://www.google.com/search?q={} wiki'.format(msg)).text
    page = fromstring(raw)

    link = ''

    for result in pg.cssselect(".r a"):
        url = result.get("href")
        if url.startswith("/url?"):
            url = parse_qs(urlparse(url).query)['q']
        if "wikipedia" in url[0]:
            link = url[0]
            break

    raw = get(link).text
    page = fromstring(raw)

    if len(page.cssselect(".longitude")) == 0:

        result[index] = {}
        return True

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

    result[index] = {'info': information, 'name': name, 'latitude': latitude, 'longitude': longitude}
    return True

def find_coordinates (msg, result, index):


    raw = get('https://en.wikipedia.org/wiki/{}'.format(msg)).text
    page = fromstring(raw)

    if len(page.cssselect(".longitude")) == 0:

        return find_coordinates_alt(msg, result, index)

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

    result[index] = {'info': information, 'name': name, 'latitude': latitude, 'longitude': longitude}
    return True

def setup(client):
    client.add_cog(Google(client))
