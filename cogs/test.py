from discord.ext import commands
import discord

class TestErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='test')
    async def test_error_command(self, ctx, error_type: str):
        """test用のコマンドだにぇ"""
        if error_type == "CommandNotFound":
            await ctx.message.add_reaction('\u2705')
            raise commands.CommandNotFound("これはテスト用のコマンドが見つからないエラーです。")
        elif error_type == "MissingRequiredArgument":
            await ctx.message.add_reaction('\u2705')
            raise commands.MissingRequiredArgument(param=None)
        elif error_type == "TooManyArguments":
            await ctx.message.add_reaction('\u2705')
            raise commands.TooManyArguments("引数が多すぎます。")
        elif error_type == "BadArgument":
            await ctx.message.add_reaction('\u2705')
            raise commands.BadArgument("無効な引数が提供されました。")
        elif error_type == "NoPrivateMessage":
            await ctx.message.add_reaction('\u2705')
            raise commands.NoPrivateMessage("このコマンドはプライベートメッセージでは使用できません。")
        elif error_type == "PrivateMessageOnly":
            await ctx.message.add_reaction('\u2705')
            raise commands.PrivateMessageOnly("このコマンドはプライベートメッセージでのみ使用できます。")
        elif error_type == "NotOwner":
            await ctx.message.add_reaction('\u2705')
            raise commands.NotOwner("このコマンドはBotのオーナーのみが使用できます。")
        elif error_type == "MissingPermissions":
            await ctx.message.add_reaction('\u2705')
            # MissingPermissions エラーは通常、特定の権限が欠けている場合に発生します。
            # この例ではダミーの権限リストを使用していますが、実際には適切な権限を指定する必要があります。
            raise commands.MissingPermissions(["manage_messages"])
        elif error_type == "BotMissingPermissions":
            await ctx.message.add_reaction('\u2705')
            # BotMissingPermissions エラーはBotが必要とする権限が欠けている場合に発生します。
            # この例ではダミーの権限リストを使用していますが、実際には適切な権限を指定する必要があります。
            raise commands.BotMissingPermissions(["manage_messages"])
        elif error_type == "CheckFailure":
            await ctx.message.add_reaction('\u2705')
            raise commands.CheckFailure("コマンドの前提条件を満たしていません。")
        elif error_type == "CommandOnCooldown":
            await ctx.message.add_reaction('\u2705')
            # CommandOnCooldown エラーはコマンドがクールダウン中に再度実行された場合に発生します。
            # この例ではダミーの再試行時間を設定していますが、実際には適切な設定が必要です。
            raise commands.CommandOnCooldown(cooldown=discord.Cooldown(rate=1, per=30, type=commands.BucketType.user), retry_after=30)
        elif error_type == "DisabledCommand":
            await ctx.message.add_reaction('\u2705')
            raise commands.DisabledCommand("このコマンドは現在無効になっています。")
        elif error_type == "CommandInvokeError":
            await ctx.message.add_reaction('\u2705')
            # CommandInvokeError エラーはコマンドの実行中に発生したエラーをラップするために使用されます。
            # この例では単純なRuntimeErrorを発生させていますが、実際にはさまざまな原因が考えられます。
            raise commands.CommandInvokeError(original=RuntimeError("コマンド実行中にエラーが発生しました。"))

        else:
            await ctx.respond(f"指定されたエラータイプ `{error_type}` はサポートされていません。", ephemeral=True)

    @commands.hybrid_command(name='test_list')
    async def test_list(self, ctx):
        """test用のコマンド一覧だにぇ"""
        e = discord.Embed(
            title="Testコマンドの一覧",
            color=0xFF8FDF
        )
        e.add_field(
            name="CommandNotFound",
            value="コマンドが見つからないにぇ"
        )
        e.add_field(
            name="MissingRequiredArgument",
            value="必要な引数が不足してるにぇ"
        )
        e.add_field(
            name="TooManyArguments",
            value="引数が多すぎるにぇ"
        )
        e.add_field(
            name="BadArgument",
            value="無効な引数が提供されたにぇ"
        )
        e.add_field(
            name="NoPrivateMessage",
            value="このコマンドはプライベートメッセージでは使えないにぇ"
        )
        e.add_field(
            name="PrivateMessageOnly",
            value="このコマンドはプライベートメッセージでのみ使えるにぇ"
        )
        e.add_field(
            name="NotOwner",
            value="このコマンドはBotのオーナーのみが使えるにぇ"
        )
        e.add_field(
            name="MissingPermissions",
            value="必要な権限がないみたいだにぇ"
        )
        e.add_field(
            name="BotMissingPermissions",
            value="Botに必要な権限がないみたいだにぇ"
        )
        e.add_field(
            name="CheckFailure",
            value="コマンドの前提条件を満たしていません。"
        )
        e.add_field(
            name="CommandOnCooldown",
            value="コマンドはクールダウン中だにぇ。"
        )
        e.add_field(
            name="DisabledCommand",
            value="このコマンドは現在無効になっているにぇ"
        )
        e.add_field(
            name="CommandInvokeError",
            value="コマンド実行中にエラーが発生したにぇ"
        )
        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(TestErrorCog(bot))
