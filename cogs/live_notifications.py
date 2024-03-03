from discord.ext import tasks, commands
import os
import googleapiclient.discovery

class LiveNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'ここにYouTubeチャンネルIDを入力'  # 監視対象のYouTubeチャンネルID
        self.DISCORD_CHANNEL_ID = 1213703226143019069
        self.check_live_status.start()

    @tasks.loop(minutes=60)
    async def check_live_status(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)
        
        request = youtube.liveBroadcasts().list(
            part="snippet",
            broadcastStatus="active",
            broadcastType="all",
            channelId=self.CHANNEL_ID
        )
        response = request.execute()

        if response['items']:
            for item in response['items']:
                live_status = item['snippet']['liveBroadcastContent']
                if live_status == 'live':
                    video_id = item['id']
                    video_title = item['snippet']['title']
                    video_url = f'https://www.youtube.com/watch?v={video_id}'
                    message = f'🔴 **ライブ放送開始** 🔴\nタイトル: {video_title}\nURL: {video_url}'
                    channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
                    await channel.send(message)

    @check_live_status.before_loop
    async def before_check_live_status(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(LiveNotifications(bot))


