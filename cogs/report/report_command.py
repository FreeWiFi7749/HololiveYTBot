import discord
from discord.ext import commands
import os
import json
from pathlib import Path

class ReportCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_report_path = '/data/report/dm_message'
        self.config_path = 'data/report/config.json'

    def load_report_channel_id(self, guild_id):
        """設定ファイルから通報チャンネルのIDを読み込む"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            guild_config = config.get(str(guild_id))
            if guild_config:
                return guild_config.get("report_channel")
        return None

    async def send_reports(self, ctx, reason):
        self.report_channel_id = self.load_report_channel_id(ctx.guild.id)
        if not self.report_channel_id:
            await ctx.send("通報チャンネルが設定されていません。", ephemeral=True)
            return
        
        reports = []
        for user_dir in os.listdir(self.base_report_path):
            user_path = Path(self.base_report_path) / user_dir
            if user_path.is_dir():
                for report_file in user_path.iterdir():
                    with open(report_file, 'r') as f:
                        reports.append(json.load(f))

        reports.sort(key=lambda x: x['message_id'])

        for report in reports:
            e = discord.Embed(title="通報されたメッセージ", description=report['content'], color=discord.Color.red())
            e.add_field(name="通報されたユーザー", value=f"<@{report['author_id']}>")
            e.add_field(name="通報したユーザー", value=f"<@{report['reporter_id']}>")
            e.add_field(name="理由", value=reason)
            report_channel = self.bot.get_channel(int(self.report_channel_id))
            if report_channel:
                await report_channel.send(embed=e)

        await ctx.send("通報が完了しました。", ephemeral=True)

    @commands.hybrid_command(name="report")
    async def report_command(self, ctx, *, reason: str):
        """通報を完了する"""
        await self.send_reports(ctx, reason)

async def setup(bot):
    await bot.add_cog(ReportCommand(bot))