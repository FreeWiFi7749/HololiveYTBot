import discord
from discord.ext import commands
import io
import textwrap
from contextlib import redirect_stdout
import traceback
from discord.ext.commands import Context

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content

    @commands.hybrid_command(hidden=True, with_app_command=True, name='_eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """管理者用コマンドだにぇ"""
        if not ctx.interaction:
            body = self.cleanup_code(body)
        
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }

        env.update(globals())

        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except discord.HTTPException:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.hybrid_command(name='clear', with_app_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        """言われた数のメッセージを削除するにぇ"""
        if not ctx.interaction:
            deleted = await ctx.channel.purge(limit=limit)
            message = f'削除されたメッセージの数: `{len(deleted)}`'
            await ctx.send(message, delete_after=5)
        else:
            await ctx.defer(ephemeral=True)
            deleted = await ctx.channel.purge(limit=limit)
            message = f'削除されたメッセージの数: `{len(deleted)}`'
            await ctx.send(message, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
