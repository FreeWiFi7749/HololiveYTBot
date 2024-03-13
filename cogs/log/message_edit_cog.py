import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

class MessageEditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def shorten_text(self, text, max_length=1024):
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        # ボットが送信したメッセージは無視する
        if message_before.author.bot:
            return

        # メッセージの内容が変更されていない場合は無視する
        if message_before.content == message_after.content:
            return

        # 現在の時刻を取得
        JST = timezone(timedelta(hours=+9))

        # ログを埋め込みメッセージとして作成
        embed = discord.Embed(title="メッセージ編集ログ", color=discord.Color.green(), timestamp=message_before.created_at )
        embed.add_field(name="編集前", value=self.shorten_text(message_before.content), inline=True)
        embed.add_field(name="編集後", value=self.shorten_text(message_after.content), inline=True)
        embed.add_field(name="チャンネル", value="\n"+message_before.channel.mention + f"\n[メッセージに飛ぶ]({message_after.jump_url})", inline=True)
        embed.set_author(icon_url=message_before.author.avatar, name=message_before.author.display_name)
        embed.set_footer(text="メッセージID | " + str(message_before.id))

        client = discord.Client()  # Replace with the appropriate client initialization

        thread_id = 1128694821935141105
        thread = await client.fetch_channel(thread_id)

        if thread is None or not isinstance(thread, discord.Thread):
            return

        try:
            await thread.send(embed=embed)
        except discord.Forbidden:
            return

async def setup(bot):
    await bot.add_cog(MessageEditCog(bot))