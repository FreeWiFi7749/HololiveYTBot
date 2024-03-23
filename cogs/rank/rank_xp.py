from discord.ext import commands
import json
import os
import random

class RankXP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.xp_path = 'data/rank/xp/user/'
        os.makedirs(self.xp_path, exist_ok=True)

    def add_xp(self, user_id, username):
        xp_to_add = 10
        user_xp_file = f'{self.xp_path}{username}.json'

        if not os.path.exists(user_xp_file):
            user_data = {'xp': 0, 'level': 1}
        else:
            with open(user_xp_file, 'r') as f:
                user_data = json.load(f)

        if random.random() < 0.1:
            user_data['xp'] += xp_to_add

            with open(user_xp_file, 'w') as f:
                json.dump(user_data, f)
            return True
        return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        #if self.add_xp(message.author.id, message.author.name):
        #    await message.channel.send(f'{message.author.mention} にXPを付与しました！')

async def setup(bot):
    await bot.add_cog(RankXP(bot))