import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone
import discord
from discord.ext import commands
from datetime import datetime, timedelta, timezone

class MemberJoinLeaveCog(commands.Cog):
    class MemberJoinLeaveCog(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_member_join(self, member):
            thread_id = 1217304524067311686
            thread = await self.bot.fetch_channel(thread_id)
        
            JST = timezone(timedelta(hours=+9))
            now = datetime.now(JST)

            created_at = member.joined_at.replace(tzinfo=timezone.utc).astimezone(JST)

            embed = discord.Embed(title="ユーザー参加ログ", color=discord.Color.green(), timestamp=now )
            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.add_field(name="ユーザー名", value=member.display_name + "\n" + member.mention, inline=True)
            embed.add_field(name="ユーザーID", value=str(member.id), inline=True)

            nownow = datetime.now(JST)
            created_at_timestamp = created_at.timestamp()
            account_age = nownow.timestamp() - created_at_timestamp

            embed.add_field(name="アカウント年齢", value=now.strftime('%Y/%m/%d  %H:%M:%S') + f"| <t:{int(account_age)}:R>", inline=True)

            await thread.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        thread_id = 1217304524067311686
        thread = await self.bot.fetch_channel(thread_id)
        guild = member.guild
        JST = timezone(timedelta(hours=+9))
        now = datetime.now(JST)
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
            if discord.utils.utcnow() - entry.created_at < timedelta(minutes=1):
                thread_id = 1217304390470205460
                thread = await self.bot.fetch_channel(thread_id)
                if entry.reason == None:
                    reason = "なし"
                else:
                    reason = entry.reason
                embed = discord.Embed(title="ユーザーキックログ", color=discord.Color.orange(), timestamp=now)
                embed.set_author(name=member.name, icon_url=member.avatar)
                embed.add_field(name="ユーザー名", value=member.mention, inline=True)
                embed.add_field(name="ユーザーID", value=member.id, inline=True)
                embed.add_field(name="実行者", value=entry.user.mention, inline=True)
                embed.add_field(name="理由", value=reason, inline=True)  
                await thread.send(embed=embed)
                break
            else:
                embed = discord.Embed(title="ユーザー退出ログ", color=discord.Color.red(), timestamp=now)
                embed.set_author(name=member.name, icon_url=member.avatar)
                embed.add_field(name="ユーザー名", value=member.display_name + "\n" + member.mention, inline=True)
                embed.add_field(name="ユーザーID", value=member.id, inline=True)
                await thread.send(embed=embed)
                return

async def setup(bot):
    await bot.add_cog(MemberJoinLeaveCog(bot))
