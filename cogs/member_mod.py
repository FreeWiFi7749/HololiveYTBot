import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Membermod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def banlist(self, ctx):
        """Banされたユーザーのリストを表示するにぇ"""
        exclude_names = ["Deleted User", "deleted_user"]
        ban_entries = []
        async for ban_entry in ctx.guild.bans():
            if not any(exclude_name.lower() in ban_entry.user.name.lower() for exclude_name in exclude_names):
                ban_entries.append(ban_entry)

        message_lines = [f"<@{ban_entry.user.id}> | {ban_entry.user.id}" for ban_entry in ban_entries]

        if message_lines:
            for i in range(0, len(message_lines), 10):
                await ctx.send("\n".join(message_lines[i:i+10]))
        else:
            await ctx.send("Banされたユーザーはいません。")

async def setup(bot):
    await bot.add_cog(Membermod(bot))