from discord.ext import tasks, commands
import discord
from dotenv import load_dotenv
import os
import googleapiclient.discovery
from datetime import datetime, timedelta
import pytz
import json

load_dotenv()

class VideoNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DISCORD_CHANNEL_ID = 1213703241867730945
        self.last_check = self.load_last_check()
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'UC-hM6YJuNYVAmUWxeIr9FeA'
        self.check_new_videos.start()

    def load_last_check(self):
        try:
            with open("data/last_check.json", "r") as file:
                data = json.load(file)
                return datetime.fromisoformat(data["last_check"])
        except (FileNotFoundError, json.JSONDecodeError):
            return datetime.now(pytz.UTC) - timedelta(days=1)

    def save_last_check(self):
        os.makedirs("data", exist_ok=True)
        with open("data/last_check.json", "w") as file:
            json.dump({"last_check": self.last_check.isoformat()}, file)

    @tasks.loop(minutes=60)
    async def check_new_videos(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        
        request = youtube.search().list(
            part="snippet",
            channelId=self.CHANNEL_ID,
            type="video",
            publishedAfter=self.last_check.isoformat(),
            maxResults=5,
            order="date"
        )
        response = request.execute()

        if response['items']:
            for item in response['items']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                message = f'🆕 **新しい動画が投稿されました** 🆕\nタイトル: {video_title}\nURL: {video_url}'
                channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
                await channel.send(message)
            
            self.last_check = datetime.now(pytz.UTC)
            self.save_last_check()

    @check_new_videos.before_loop
    async def before_check_new_videos(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(VideoNotifications(bot))