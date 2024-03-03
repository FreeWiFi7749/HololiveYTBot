import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
import os
import googleapiclient.discovery
from googleapiclient.discovery import HttpError
from datetime import datetime, timedelta, timezone
import asyncio

load_dotenv()

class SubscriberNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'UC-hM6YJuNYVAmUWxeIr9FeA'
        self.DISCORD_CHANNEL_ID = 1213703288193683526
        self.check_subscribers.start()

    async def send_quota_exceeded_message(self):
        channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
        if channel:
            await channel.send("⚠️ YouTube APIのクォータ制限に達しました。しばらくの間、登録者数の通知は行われません。")

    @tasks.loop(hours=24)
    async def check_subscribers(self):
        try:
            youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        
            # チャンネルの登録者数を取得
            request = youtube.channels().list(
                part="statistics",
                id=self.CHANNEL_ID
            )
            response = request.execute()
        
            if response['items']:
                subscriber_count = int(response['items'][0]['statistics']['subscriberCount'])
                message = f'📈 現在の登録者数: {subscriber_count}人'
                if subscriber_count % 10000 == 0:
                    channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
                    await channel.send(f'🎉 **登録者数が{subscriber_count}人に到達しました!** 🎉\n{message}')

        except HttpError as e:
            if e.resp.status in [403, 429]:
                await self.send_quota_exceeded_message()
                await asyncio.sleep(60 * 60)
            else:
                raise
            
    @check_subscribers.before_loop
    async def before_check_subscribers(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(SubscriberNotifications(bot))
