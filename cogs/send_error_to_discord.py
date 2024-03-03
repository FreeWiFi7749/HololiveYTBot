import discord
from discord.ext import tasks, commands
import json
from googleapiclient.discovery import HttpError
from pathlib import Path

class ErrorHandlingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main_channel_id = 1213768790136066078
        self.error_threads = self.load_error_threads()

    def load_error_threads(self):
        path = Path('data/error_threads.json')
        if path.is_file():
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}

    def save_error_threads(self):
        path = Path('data/error_threads.json')
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.error_threads, f, ensure_ascii=False, indent=4)

    async def get_or_create_thread(self, error_name):
        main_channel = self.bot.get_channel(self.main_channel_id)
        if not main_channel:
            print("メインチャンネルが見つかりません。")
            return None

        # スレッド名から既存のスレッドを検索
        for thread in await main_channel.threads():
            if thread.name == error_name:
                return thread

        # 該当するスレッドがない場合、新しく作成
        thread = await main_channel.create_thread(name=error_name, type=discord.ChannelType.public_thread)
        self.error_threads[error_name] = thread.id
        self.save_error_threads()
        return thread

    async def notify_error(self, error_type, message):
        thread = await self.get_or_create_thread(error_type)
        if thread:
            await thread.send(message)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await self.notify_error('command_not_found', f"```{error}```\n\nコマンドが見つかりません: {ctx.message.content}")
        elif isinstance(error, commands.MissingRequiredArgument):
            await self.notify_error('missing_required_argument', f"```{error}```\n\n必要な引数が不足しています: {ctx.message.content}")
        elif isinstance(error, commands.TooManyArguments):
            await self.notify_error('too_many_arguments', f"```{error}```\n\n引数が多すぎます。")
        elif isinstance(error, commands.BadArgument):
            await self.notify_error('bad_argument', f"```{error}```\n\n無効な引数が提供されました。")
        elif isinstance(error, commands.NoPrivateMessage):
            await self.notify_error('no_private_message', f"```{error}```\n\nこのコマンドはプライベートメッセージでは使用できません。")
        elif isinstance(error, commands.PrivateMessageOnly):
            await self.notify_error('private_message_only', f"```{error}```\n\nこのコマンドはプライベートメッセージでのみ使用できます。")
        elif isinstance(error, commands.NotOwner):
            await self.notify_error('not_owner', f"```{error}```\n\nこのコマンドはBotのオーナーのみが使用できます。")
        elif isinstance(error, commands.MissingPermissions):
            await self.notify_error('missing_permissions', f"```{error}```\n\n必要な権限がありません。")
        elif isinstance(error, commands.BotMissingPermissions):
            await self.notify_error('bot_missing_permissions', f"```{error}```\n\nBotに必要な権限がありません。")
        elif isinstance(error, commands.CheckFailure):
            await self.notify_error('check_failure', f"```{error}```\n\nコマンドの前提条件を満たしていません。")
        elif isinstance(error, commands.CommandOnCooldown):
            await self.notify_error('command_on_cooldown', f"```{error}```\n\nコマンドはクールダウン中です。再試行まで: {error.retry_after:.2f}秒。")
        elif isinstance(error, commands.DisabledCommand):
            await self.notify_error('disabled_command', "```{error}```\n\nこのコマンドは現在無効になっています。")
        elif isinstance(error, commands.CommandInvokeError):
            await self.notify_error('command_invoke_error', f"```{error}```\n\nコマンド実行中にエラーが発生しました: {error.original}")
        # その他のエラータイプに対する処理を追加...
        else:
            await self.notify_error('unknown_error', f"```{error}```\n\n未知のエラーが発生しました。")

    async def handle_api_error(self, error):
        if isinstance(error, HttpError):
            if error.resp.status in [403, 429]:
                await self.notify_error('quota_exceeded', "YouTube APIのクォータ制限に達しました。")
            else:
                await self.notify_error('unknown_api_error', str(error))

async def setup(bot):
    await bot.add_cog(ErrorHandlingCog(bot))
