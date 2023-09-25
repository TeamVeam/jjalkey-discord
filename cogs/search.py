import os

import discord
from discord.commands import Option
from discord.ext import commands, pages
import aiohttp

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('JJALKEY_API_KEY')
API_URL = "https://api.jjalkey.com/v1/search?api_key=" + API_KEY + "&q="


class JjalkeySearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="검색", description="검색어와 일치하는 태그를 가진 짤을 가져옵니다.")
    async def search(self, ctx, query: Option(str, name="검색어", description="검색어를 입력하세요.", required=True)):
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL + query) as resp:
                if resp.status == 200:
                    jjal_list = []
                    jjal_json = (await resp.json())['data']

                    for _, item in enumerate(jjal_json):
                        jjal_list.append(item['url'])

                    if not jjal_list:
                        await ctx.respond("검색 결과가 없습니다.")
                    else:
                        paginator = pages.Paginator(pages=jjal_list)
                        await paginator.respond(ctx.interaction)


def setup(bot):
    bot.add_cog(JjalkeySearch(bot))
