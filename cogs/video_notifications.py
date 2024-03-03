from discord.ext import tasks, commands
import os
import googleapiclient.discovery
from datetime import datetime, timedelta
import pytz

class VideoNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'ここにYouTubeチャンネルIDを入力'  # 監視対象のYouTubeチャンネルID
        self.DISCORD_CHANNEL_ID = 1213703241867730945
        self.last_check = datetime.now(pytz.UTC) - timedelta(days=1)  # 最後にチェックした日時（デフォルトは1日前）
        self.check_new_videos.start()

    @tasks.loop(minutes=60)
    async def check_new_videos(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        
        # 最後にチェックした日時以降にアップロードされた動画を検索
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
            
            # 最後にチェックした日時を更新
            self.last_check = datetime.now(pytz.UTC)

    @check_new_videos.before_loop
    async def before_check_new_videos(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(VideoNotifications(bot))
