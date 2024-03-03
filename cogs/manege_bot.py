import discord
from discord.ext import commands
import os
import sys
import subprocess
import platform
import asyncio

class ManagementBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def rstart_bot(self):
        try:
            if platform.system() == "Linux":
                subprocess.Popen(["/bin/sh", "-c", "sleep 1; exec python3 " + " ".join(sys.argv)])
            elif platform.system() == "Darwin":
                subprocess.Popen(["/bin/sh", "-c", "sleep 1; exec python3 " + " ".join(sys.argv)])
            else:
                print("このOSはサポートされていません。")
                return
            await self.bot.close()
        except Exception as e:
            print(f"再起動中にエラーが発生しました: {e}")


    @commands.hybrid_command(name='restart')
    @commands.is_owner()
    async def restart(self, ctx):
        """Botを再起動するにぇ"""
        msg = await ctx.send('10秒後にBotを再起動するにぇ...')
        for i in range(9, 0, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f"{i}秒後にBotを再起動するにぇ...")
            if i == 1:
                await msg.edit(content=f"再起動をするにぇ‼️")
                
        await self.rstart_bot()

async def setup(bot):
    await bot.add_cog(ManagementBot(bot))