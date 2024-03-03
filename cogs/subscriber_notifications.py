from discord.ext import tasks, commands
import os
import googleapiclient.discovery

class SubscriberNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'ここにYouTubeチャンネルIDを入力'  # 監視対象のYouTubeチャンネルID
        self.DISCORD_CHANNEL_ID = 1213703288193683526
        self.check_subscribers.start()

    @tasks.loop(hours=24)
    async def check_subscribers(self):
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
            # 特定のマイルストーンで通知を送る
            if subscriber_count % 10000 == 0:  # ここでは1000人ごとの登録者数で通知を送る例を示しています
                channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
                await channel.send(f'🎉 **登録者数が{subscriber_count}人に到達しました!** 🎉\n{message}')

    @check_subscribers.before_loop
    async def before_check_subscribers(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(SubscriberNotifications(bot))
