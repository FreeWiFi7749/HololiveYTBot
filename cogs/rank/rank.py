import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import json
import os
import aiohttp
from io import BytesIO
import io

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_path = 'data/rank/xp/user/'
        self.bg_image_path = 'resource/image/rank/default_bg.png'
        self.font_path = 'resource/font/rank/ZenMaruGothic-Light.ttf'
        self.max_xp_bar_width = 400

    def load_user_data(self, user_id):
        user_data_file = f'{self.data_path}{user_id}.json'
        if not os.path.exists(user_data_file):
            return {'xp': 0, 'level': 1}
        with open(user_data_file, 'r') as f:
            return json.load(f)

    def process_level_up(self, user_data):
        xp_for_next_level = (user_data['level'] ** 2) * 100
        if user_data['xp'] >= xp_for_next_level:
            user_data['xp'] -= xp_for_next_level
            user_data['level'] += 1
            return True
        return False

    def calculate_xp_bar_length(self, xp, level, max_width=400):
        xp_for_next_level = (level ** 2) * 100
        return int((xp / xp_for_next_level) * max_width)

    @commands.hybrid_command(name="rank")
    async def rank(self, ctx):
        """ユーザーのランクを表示するにぇ"""
        user_id = str(ctx.author.id)
        user_data = self.load_user_data(user_id)

        async with aiohttp.ClientSession() as session:
            async with session.get(str(ctx.author.avatar.url)) as resp:
                if resp.status != 200:
                    return await ctx.send('アバターをロードできませんでした。')
                avatar_data = BytesIO(await resp.read())
                avatar_image = Image.open(avatar_data)

        with Image.open(self.bg_image_path) as bg_image:
            bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))

            avatar_image = avatar_image.resize((100, 100))
            mask = Image.new('L', avatar_image.size, 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0) + avatar_image.size, fill=255)
            avatar_image.putalpha(mask)

            bg_image.paste(avatar_image, (10, 10), avatar_image)

            draw = ImageDraw.Draw(bg_image)
            font = ImageFont.truetype(self.font_path, 20)

            draw.text((120, 10), f"{ctx.author.display_name}", (0, 0, 0), font=font)
            draw.text((120, 40), f"レベル: {user_data['level']}", (0, 0, 0), font=font)

            xp_bar_back_color = (255, 255, 255, 128)
            draw.rectangle([(120, 70), (120 + self.max_xp_bar_width, 70 + 20)], fill=xp_bar_back_color)

            xp_bar_length = self.calculate_xp_bar_length(user_data['xp'], user_data['level'], self.max_xp_bar_width)
            xp_bar_color = (191, 0, 255)
            draw.rectangle([(120, 70), (120 + xp_bar_length, 70 + 20)], fill=xp_bar_color)

            temp_image_path = f'temp/{ctx.author.id}_rank.png'
            bg_image.save(temp_image_path)

            discord_file = discord.File(temp_image_path, filename="rank.png")

            await ctx.send(file=discord_file)
            os.remove(temp_image_path)

async def setup(bot):
    await bot.add_cog(Rank(bot))