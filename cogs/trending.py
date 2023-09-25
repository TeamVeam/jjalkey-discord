import os

import discord
from discord.ext import commands, pages
import aiohttp

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('JJALKEY_API_KEY')
API_URL = "https://api.jjalkey.com/v1/trending?api_key=" + API_KEY


class JjalkeyTrending(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="인기", description="인기 짤을 순서대로 가져옵니다.")
    async def trending(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                if resp.status == 200:
                    jjal_list = []
                    jjal_json = (await resp.json())['data']

                    for _, item in enumerate(jjal_json):
                        jjal_list.append(item['url'])

                    paginator = pages.Paginator(pages=jjal_list)
                    await paginator.respond(ctx.interaction)


def setup(bot):
    bot.add_cog(JjalkeyTrending(bot))
