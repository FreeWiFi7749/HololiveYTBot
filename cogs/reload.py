from discord.ext import commands
import discord

class ManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog: str):
        """Reloads a specified cog."""
        try:
            self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"Reloaded cog: {cog}")
        except Exception as e:
            await ctx.send(f"Failed to reload cog: {cog}\n{type(e).__name__}: {e}")

async def setup(bot):
    await bot.add_cog(ManagementCog(bot))
