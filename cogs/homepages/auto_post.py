from discord.ext import commands
import aiohttp
from datetime import datetime
import pytz
from urllib.parse import urljoin

WP_URL = 'http://hfs-dev.local/'
WP_USERNAME = 'freewifi'
WP_PASSWORD = 'arGb 2mri scxh EwuP RD5Z vb0k'

class AutoPoster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def post_article(self, status, slug, title, content, category_ids, tag_ids, media_id):
        async with aiohttp.ClientSession() as session:
            payload = {
                "status": status,
                "slug": slug,
                "title": title,
                "content": content,
                "date": datetime.now(pytz.timezone('Asia/Tokyo')).isoformat(),
                "categories": category_ids,
                "tags": tag_ids
            }
            if media_id is not None:
                payload['featured_media'] = media_id

            async with session.post(
                urljoin(WP_URL, "wp-json/wp/v2/posts"),
                json=payload,
                auth=aiohttp.BasicAuth(WP_USERNAME, WP_PASSWORD),
                timeout=10
            ) as response:
                text = await response.text()
                if response.status == 201:
                    print(f"記事 '{title}' を投稿しました。")
                else:
                    print(f"記事 '{title}' の投稿に失敗しました。エラー: {text}")

    @commands.Cog.listener()
    async def on_guild_scheduled_event_create(self, event):
        title = event.name
        image_url = event.cover_url if event.cover_url else "デフォルトの画像URL"
        content = f'<img src="{image_url}"/><p>イベント作成時間: {datetime.now(pytz.timezone("Asia/Tokyo")).isoformat()}</p>'

        # Call the async post_article method directly with await
        await self.post_article('publish', 'event-slug', title, content, [2], [], None)

async def setup(bot):
    await bot.add_cog(AutoPoster(bot))