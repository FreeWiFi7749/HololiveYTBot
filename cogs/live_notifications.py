import discord
from discord.ext import tasks, commands
import googleapiclient.discovery
from googleapiclient.discovery import build
import os
from utils.get_cahnnel_icon import get_channel_icon_url

class LiveNotifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
        self.CHANNEL_ID = 'UC-hM6YJuNYVAmUWxeIr9FeA'
        self.DISCORD_CHANNEL_ID = 1213703226143019069
        self.check_live_status.start()

    async def notify_discord(self, item, status):
        """Discordチャンネルに埋め込み通知を送信するヘルパー関数"""
        channel = self.bot.get_channel(self.DISCORD_CHANNEL_ID)
        if not channel:
            return
        
        channel_id = item['snippet']['channelId']
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_title = item['snippet']['title']
        channel_title = item['snippet']['channelTitle']
        thumbnail_url = item['snippet']['thumbnails'].get('high', {}).get('url') or item['snippet']['thumbnails'].get('standard', {}).get('url') or item['snippet']['thumbnails']['default']['url']


        channel_icon_url = get_channel_icon_url(channel_id)
        
        embed = discord.Embed(
            title=f'{video_title}',
            url=video_url,
            color=0xFF8FDF
        )
        embed.set_author(name=channel_title, icon_url=channel_icon_url)
        embed.set_image(url=thumbnail_url)
        print(f'サムネ画像の画質: {thumbnail_url}')
        
        if status == '終了':
            concurrent_viewers = item.get('liveStreamingDetails', {}).get('concurrentViewers', '❓❓')
            end_time = item.get('liveStreamingDetails', {}).get('actualEndTime')
            if end_time is not None:
                end_time_str = f'<t:{int(end_time)}:F>'
            else:
                end_time_str = '❓❓'
            embed.description = f'最高視聴者数: {concurrent_viewers}\n終了時刻: {end_time_str}'
        else:
            start_time = item.get('liveStreamingDetails', {}).get('scheduledStartTime')
            if start_time is not None:
                start_time_str = f'<t:{int(start_time)}:F>'
            else:
                start_time_str = '❓❓'
                embed.description = f'開始予定時刻: {start_time_str}'


        await channel.send(embed=embed)

    @tasks.loop(minutes=10)
    async def check_live_status(self):
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=self.YOUTUBE_API_KEY)

        # 予定されているライブ配信を検索
        upcoming_request = youtube.search().list(
            part="snippet",
            channelId=self.CHANNEL_ID,
            eventType="upcoming",
            type="video",
            maxResults=1
        )
        upcoming_response = upcoming_request.execute()

        # 進行中のライブ配信を検索
        live_request = youtube.search().list(
            part="snippet",
            channelId=self.CHANNEL_ID,
            eventType="live",
            type="video",
            maxResults=1
        )
        live_response = live_request.execute()

        # 終了したライブ配信を検索
        completed_request = youtube.search().list(
            part="snippet",
            channelId=self.CHANNEL_ID,
            eventType="completed",
            type="video",
            maxResults=1
        )
        completed_response = completed_request.execute()
        # ライブの枠があれば通知
        for item in upcoming_response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            live_details = item.get('liveStreamingDetails', {})
            start_time = live_details.get('scheduledStartTime')
            end_time = live_details.get('actualEndTime')
            await self.notify_discord(item, '予定')

        # 進行中のライブ配信があれば通知
        for item in live_response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            live_details = item.get('liveStreamingDetails', {})
            start_time = live_details.get('scheduledStartTime')
            end_time = live_details.get('actualEndTime')
            await self.notify_discord(item, '開始')

        # 終了したライブ配信があれば通知
        for item in completed_response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            live_details = item.get('liveStreamingDetails', {})
            start_time = live_details.get('scheduledStartTime')
            end_time = live_details.get('actualEndTime')
            await self.notify_discord(item, '終了')

    @check_live_status.before_loop
    async def before_check_live_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(LiveNotifications(bot))



