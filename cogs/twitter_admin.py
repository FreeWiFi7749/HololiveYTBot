import discord
from discord.ext import commands
import json
import os

class TwitterAdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channels_file = 'data/twitter_channels.json'
        self.config_folder = 'data/twitter_forward'
        os.makedirs(self.config_folder, exist_ok=True)
        if not os.path.exists(self.channels_file):
            with open(self.channels_file, 'w') as f:
                json.dump({'twitter_channels': []}, f, indent=4)

    def load_channels(self):
        with open(self.channels_file, 'r') as f:
            return json.load(f)['twitter_channels']

    def save_channels(self, channels):
        with open(self.channels_file, 'w', encoding='utf-8') as f:
            json.dump({'twitter_channels': channels}, f, ensure_ascii=False, indent=4)

    def config_path(self, guild_id):
        return os.path.join(self.config_folder, f'{guild_id}.json')

    def load_config(self, guild_id):
        try:
            with open(self.config_path(guild_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_config(self, guild_id, data):
        with open(self.config_path(guild_id), 'w') as f:
            json.dump(data, f, indent=4)

    @commands.hybrid_group(name='tw', invoke_without_command=True, with_app_command=True)
    async def twitter(self, ctx):
        """Twitter関連のコマンド"""
        await ctx.send_help(ctx.command)

    @twitter.command(name='addsource')
    @commands.is_owner()
    async def add_source_channel(self, ctx, channel: discord.TextChannel):
        """ソースチャンネルを追加する（Botオーナー専用）"""
        channels = self.load_channels()
        if any(c['channel_id'] == str(channel.id) for c in channels):
            await ctx.send('このチャンネルは既にソースチャンネルとして追加されているにぇ...')
            return

        channels.append({'guild_id': str(channel.guild.id), 'channel_id': str(channel.id), 'name': channel.name})
        self.save_channels(channels)
        await ctx.send(f'{channel.name} をソースチャンネルとして追加したにぇ！')

    @twitter.command(name='listsources')
    @commands.is_owner()
    async def list_source_channels(self, ctx):
        """設定されているソースチャンネルのリストを表示する（Botオーナー専用）"""
        channels = self.load_channels()
        if not channels:
            await ctx.send('ソースチャンネルが設定されていないにぇ...')
            return

        embed = discord.Embed(title="ソースチャンネルリスト", description="", color=discord.Color.blue())
        for channel in channels:
            embed.description += f'{channel["name"]} (ID: {channel["channel_id"]})\n'
        await ctx.send(embed=embed)

    @twitter.command(name='removesource')
    @commands.is_owner()
    async def remove_source_channel(self, ctx, channel_id: str):
        """ソースチャンネルを削除する（Botオーナー専用）"""
        channels = self.load_channels()
        channels = [c for c in channels if c['channel_id'] != channel_id]
        self.save_channels(channels)
        await ctx.send(f'ID {channel_id} のチャンネルをリストから削除したにぇ...')

async def setup(bot):
    await bot.add_cog(TwitterAdminCog(bot))