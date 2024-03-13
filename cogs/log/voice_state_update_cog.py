import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

class VoiceStateUpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        thread_id = 1217304473722945566
        thread = await self.bot.fetch_channel(thread_id)

        if thread is None or not isinstance(thread, discord.Thread):
            return

        JST = timezone(timedelta(hours=+9))
        now = datetime.now(JST)

        if before.channel is None and after.channel is not None:
            embed = discord.Embed(title="ボイスチャンネル入室ログ", color=discord.Color.green(), timestamp=now)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1104493356781940766/1158216598142845018/IMG_1002_adobe_express.png")
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed.add_field(name="ユーザー", value=member.mention, inline=True)
            embed.add_field(name="参加したチャンネル", value=f"{after.channel.name}\n{after.channel.mention}", inline=True)

            try:
                await thread.send(embed=embed)
            except discord.Forbidden:
                return

        elif before.channel is not None and after.channel is None:
            embed = discord.Embed(title="ボイスチャンネル退出ログ", color=discord.Color.red(), timestamp=now)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1104493356781940766/1158216598553894982/IMG_1003_adobe_express.png")
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed.add_field(name="ユーザー", value=member.mention, inline=True)
            embed.add_field(name="退出したチャンネル", value=f"{before.channel.name}\n{before.channel.mention}", inline=True)

            try:
                await thread.send(embed=embed)
            except discord.Forbidden:
                return

        elif before.channel != after.channel:
            embed = discord.Embed(title="ボイスチャンネル移動ログ", color=discord.Color.blue(), timestamp=now)
            embed.set_thumbnail(url="https://raw.githubusercontent.com/twitter/twemoji/master/assets/72x72/2195.png")
            embed.set_author(name=member.display_name, icon_url=member.avatar.url)
            embed.add_field(name="ユーザー", value=member.mention, inline=True)
            embed.add_field(name="移動前のチャンネル", value=f"{before.channel.name}\n{before.channel.mention}", inline=True)
            embed.add_field(name="移動後のチャンネル", value=f"{after.channel.name}\n{after.channel.mention}", inline=True)

            try:
                await thread.send(embed=embed)
            except discord.Forbidden:
                return
        return

async def setup(bot):
    await bot.add_cog(VoiceStateUpdateCog(bot))
