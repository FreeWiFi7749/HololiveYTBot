from discord.ext import commands
from discord import app_commands
import discord

class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='reload', with_app_command=True, hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """言われたCogを再読み込みするにぇ"""
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await self.bot.tree.sync()
            await ctx.reply(f"Reloaded cog: {cog}")
            return
        except Exception as e:
            await ctx.reply(f"Failed to reload cog: {cog}\n{type(e).__name__}: {e}")
            return

    @commands.hybrid_command(name='list_cogs', with_app_command=True)
    @commands.is_owner()
    async def list_cogs(self, ctx):
        """現在ロードされているcogsをリスト表示するにぇ"""
        embed = discord.Embed(title="ロードされているCogsのファイル名", color=discord.Color.blue())
        loaded_cogs = self.bot.cogs
        module_names = [cog_instance.__module__ for cog_instance in loaded_cogs.values()]
        embed.add_field(name="", value='\n'.join(module_names), inline=False)
        await ctx.send(embed=embed)
        return

async def setup(bot):
    await bot.add_cog(ManagementCog(bot))
