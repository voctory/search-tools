import discord
from discord.ext import commands

import lyricsgenius as genius

from datetime import datetime

import requests
import json

# load config file
with open('config.json') as data_file:
    key = json.load(data_file)["genius"]

api = genius.Genius(key)

class Genius:
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def search(self, ctx):
        words = ctx.message.clean_content.split(" ")

        # songId = api.search_genius(" ".join(words[1:]))["hits"][0]["result"]["id"]
        lyrics = api.search_song(" ".join(words[1:]))
        # print(lyrics.lyrics)

        embed = discord.Embed(title='Lyrics for "{}" by {}'.format(lyrics.title, lyrics.artist),
                description=lyrics.lyrics,
                color=0x801ecc)

        await self.client.say("", embed = embed)


def setup(client):
    client.add_cog(Genius(client))
