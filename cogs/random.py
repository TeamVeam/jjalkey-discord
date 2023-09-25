import os
from random import randrange

import discord
from discord.ext import commands, pages
import aiohttp

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('JJALKEY_API_KEY')
API_URL = "https://api.jjalkey.com/v1/random?api_key=" + API_KEY + "&limit=20" + "&s="
INT32_MAX = 2147483647


class JjalkeyRandom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="랜덤", description="랜덤 짤을 20개 가져옵니다.")
    async def random(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + str(randrange(INT32_MAX))) as resp:
                if resp.status == 200:
                    jjal_list = []
                    jjal_json = (await resp.json())['data']

                    for _, item in enumerate(jjal_json):
                        jjal_list.append(item['url'])

                    paginator = pages.Paginator(pages=jjal_list)
                    await paginator.respond(ctx.interaction)


def setup(bot):
    bot.add_cog(JjalkeyRandom(bot))
