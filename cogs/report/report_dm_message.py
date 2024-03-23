import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class ReportDmMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_report_path = "/data/report/dm_message"

    @app_commands.install_types(guild=False, users=True)
    @app_commands.allow_context(guild=False, dms=True, private_channels=True)
    @app_commands.user_command(name="通報", description="DMのメッセージをサーバー運営に通報します。")
    async def report(self, inter: discord.Interaction, message: discord.Message):
        e = discord.Embed(title="通報されたメッセージ", description=message.content, color=discord.Color.red())
        e.add_field(name="通報したユーザー", value=inter.user.mention, inline=True)
        e.add_field(name="通報されたユーザー", value=message.author.mention, inline=True)
        e.set_footer(text=f"⚠️まだ通報は完了していません⚠️\nサーバー内で/reportコマンドを使用して通報を完了してください。")
        await inter.response.send_message(embed=e, ephemeral=True)

        report_path = os.path.join(self.base_report_path, str(inter.user.id))
        if not os.path.exists(report_path):
            os.makedirs(report_path)
        
        report_file = os.path.join(report_path, f"{message.id}.json")
        report_data = {
            'message_id': message.id,
            'content': message.content,
            'author_id': message.author.id,
            'reporter_id': inter.user.id,
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=4)


async def setup(bot):
    await bot.add_cog(ReportDmMessage(bot))
