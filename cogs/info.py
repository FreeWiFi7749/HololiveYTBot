import discord
from discord.ext import commands
from datetime import datetime

class ServerInfoCog(commands.Cog, name='Server Information'):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name='info', invoke_without_command=True)
    async def info_group(self, ctx):
        """情報コマンドのグループにぇ"""
        await ctx.send("情報コマンドのサブコマンドを使ってにぇ！")

    @info_group.command(name='server')
    async def server_info(self, ctx):
        """サーバーの情報を表示するにぇ"""
        guild = ctx.guild

        number_of_text_channels = len(guild.text_channels)
        number_of_voice_channels = len(guild.voice_channels)
        number_of_stage_channels = len(guild.stage_channels)
        number_of_categories = len(guild.categories)
        
        nsfw_level = str(guild.nsfw_level).replace('_', ' ').title()
        nsfw_level = str(guild.nsfw_level).replace('Nsfwlevel.', ' ').title()

        description = (
            f'**Owner/ID:** {guild.owner} ({guild.owner_id})\n'
            f'**Created:** {guild.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'**Language:** {guild.preferred_locale}\n'
            f'**Members:** {guild.member_count}/{guild.max_members}\n'
            f'**Bots:** {sum(1 for member in guild.members if member.bot)}\n'
            f'**Roles:** {len(guild.roles)}\n'
            f'**Emojis:** {len(guild.emojis)}/{guild.emoji_limit}\n'
            f'**Stickers:** {len(guild.stickers)}/{guild.sticker_limit}\n'
            f'**Verification Level:** {str(guild.verification_level)}\n'
            f'**NSFW Level:** {nsfw_level}\n'
            f'**Channels:** \n📁 Categories: {number_of_categories}\n'
            f'💬 Text: {number_of_text_channels}\n🔊 Voice: {number_of_voice_channels}\n'
            f'🎤 Stage: {number_of_stage_channels}\n'
            f'**AFK Channel/Timeout:** {guild.afk_channel}\n{guild.afk_timeout // 60} min\n'
            f'**Boost Level:** {guild.premium_tier} (Boosters: {guild.premium_subscription_count})\n'
        )

        embed = discord.Embed(title=f'{guild.name} Server Information', description=description, color=discord.Color.blue())
        embed.set_thumbnail(url=str(guild.icon.url))

        await ctx.send(embed=embed)

    @info_group.command(name='user')
    async def user_info(self, ctx, *, user: discord.Member = None):
        """ユーザーの情報を表示するにぇ"""
        user = user or ctx.author

        if user.premium_since is not None:
            boosting_since = user.premium_since.strftime('%Y-%m-%d %H:%M:%S')
        else:
            boosting_since = 'Not boosting'
        roles_description = ", ".join(role.mention for role in user.roles[1:])

        description = f"**ID:** {user.id}\n**Created:** {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n**Joined:** {user.joined_at.strftime('%Y-%m-%d %H:%M:%S')}\n**Roles:** \n{roles_description}\n**Top Role:** {user.top_role.mention}\n**Boosting:** {boosting_since}\n"

        embed = discord.Embed(title=f'{user} User Information', description=description, color=discord.Color.blue())
        embed.set_thumbnail(url=str(user.avatar.url))

        await ctx.send(embed=embed)

    @info_group.command(name='channel')
    async def channel_info(self, ctx, *, channel: discord.abc.GuildChannel = None):
        """チャンネルの情報を表示するにぇ"""
        channel = channel or ctx.channel

        description = (
            f'**ID:** {channel.id}\n'
            f'**Created:** {channel.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'**Type:** {channel.type}\n'
        )

        embed = discord.Embed(title=f'{channel.name} Channel Information', description=description, color=discord.Color.blue())

        await ctx.send(embed=embed)
    
    @info_group.command(name='emoji')
    async def emoji_info(self, ctx, *, emoji: discord.Emoji):
        """絵文字の情報を表示するにぇ"""
        description = (
            f'**ID:** {emoji.id}\n'
            f'**Created:** {emoji.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'**URL:** [Link]({emoji.url})\n'
        )

        embed = discord.Embed(title=f'{emoji.name} Emoji Information', description=description, color=discord.Color.blue())
        embed.set_thumbnail(url=str(emoji.url))

        await ctx.send(embed=embed)
    
    @info_group.command(name='emoji_list')
    async def emoji_list(self, ctx):
        """絵文字のリストを表示するにぇ"""
        emojis_str = "\n".join(str(emoji) for emoji in ctx.guild.emojis)
        chars_per_embed = 2000

        # 絵文字リスト文字列を2000文字ごとに分割
        emojis_chunks = [emojis_str[i:i+chars_per_embed] for i in range(0, len(emojis_str), chars_per_embed)]

        for chunk in emojis_chunks:
            # 各チャンクをEmbedのdescriptionに設定して送信
            embed = discord.Embed(title="Emoji List", description=chunk, color=discord.Color.blue())
            await ctx.send(embed=embed)

    @info_group.command(name='role')
    async def role_info(self, ctx, *, role: discord.Role):
        """役職の情報を表示するにぇ"""
        description = (
            f'**ID:** {role.id}\n'
            f'**Created:** {role.created_at.strftime("%Y-%m-%d %H:%M:%S")}\n'
            f'**Color:** {role.color}\n'
            f'**Permissions:** {role.permissions}\n'
            f'**Position:** {role.position}\n'
        )

        embed = discord.Embed(title=f'{role.name} Role Information', description=description, color=role.color)
        embed.set_thumbnail(url=str(ctx.guild.icon.url))

        await ctx.send(embed=embed)
    

async def setup(bot):
    await bot.add_cog(ServerInfoCog(bot))