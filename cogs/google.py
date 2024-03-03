import os
import discord
from discord.ext import commands
import requests


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

class GoogleSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='search', help='Googleで検索するにぇ')
    async def search(self, ctx, *, query: str):
        search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': GOOGLE_API_KEY,
            'cx': GOOGLE_CSE_ID,
            'q': query,
            'num': 5,
            'lr': 'lang_ja'
        }
        
        response = requests.get(search_url, params=params)
        search_results = response.json()

        embed = discord.Embed(title=f"'{query}'の検索結果", description="", color=discord.Color.blue())
        for item in search_results.get('items', []):
            embed.add_field(name=item['title'], value=item['link'], inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GoogleSearch(bot))