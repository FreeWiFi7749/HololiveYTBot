import discord
from discord.ext import commands
import aiohttp
from PIL import Image
import io
import math

class MessageDeletionCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_image(self, session, url):
        async with session.get(url) as response:
            return await response.read()

    @commands.Cog.listener()
    async def on_message_delete(self, message):  # Added self as the first argument
        if message.author.bot:
            return
        if message.channel.name == "📮┫グローバルチャット":
            return
        guild = message.guild
        deleter = None

        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            if entry.target.id == message.author.id and entry.extra.channel.id == message.channel.id:
                deleter = entry.user
                break

        embed = discord.Embed(title="メッセージ消去ログ", color=discord.Color.red(), timestamp=message.created_at)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar)
        embed.add_field(name="メッセージ", value=f"`{message.content}`" or "なし", inline=False)
        embed.add_field(name="チャンネル", value=message.channel.mention, inline=True)
        embed.set_footer(text="メッセージID | " + str(message.id))
        if deleter:
            embed.add_field(name="消去者", value=deleter.mention, inline=True)
        else:
            embed.add_field(name="消去者", value=message.author.mention, inline=True)

        attachment_urls = [attachment.url for attachment in message.attachments]
        if len(attachment_urls) > 0:
            async with aiohttp.ClientSession() as session:
                images = []
                image_links = []
                max_width = 0
                max_height = 0
                for i, attachment_url in enumerate(attachment_urls[:10], start=1):
                    image_bytes = await self.fetch_image(session, attachment_url)  # Added self
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)
                    image_links.append(f"[画像{i}]({attachment_url})")

                    # 最大の画像サイズを取得
                    max_width = max(max_width, image.width)
                    max_height = max(max_height, image.height)

                num_images = len(images)
                max_images_per_row = 2
                max_rows = math.ceil(num_images / max_images_per_row)

                merged_width = max_width * max_images_per_row
                merged_height = max_height * max_rows

                merged_image = Image.new("RGB", (merged_width, merged_height), (255, 255, 255))

                for i, image in enumerate(images):
                    resized_image = image.resize((max_width, max_height))
                    x_offset = (i % max_images_per_row) * max_width
                    y_offset = (i // max_images_per_row) * max_height
                    merged_image.paste(resized_image, (x_offset, y_offset))

                with io.BytesIO() as output:
                    merged_image.save(output, format='PNG')
                    output.seek(0)
                    file = discord.File(output, filename="merged_images.png")

                    channel = self.bot.get_channel(1217304059535687690)  # Replaced client with self.bot
                    thread = None

                    for existing_thread in channel.threads:
                        if existing_thread.id == 1128694821935141105:
                            thread = existing_thread
                            break

                    if thread is None:
                        return

                    await thread.send(embed=embed)  # スレッドにメッセージを投稿
                    await thread.send("`消去された画像`")
                    await thread.send(file=file)  # スレッドに画像を投稿

        else:
            embed.add_field(name="添付ファイル", value="なし", inline=False)

            channel = message.guild.get_channel(1128694609980174467)  # Replaced self.get_channel with message.guild.get_channel
            thread = None

            for existing_thread in channel.threads:
                if existing_thread.id == 1128694821935141105:
                    thread = existing_thread
                    break

            if thread is None:
                return

            await thread.send(embed=embed)
            return

    def shorten_text(self, text, max_length=1024):  # Added self as the first argument
        if len(text) > max_length:
            return text[:max_length-3] + "..."
        return text

        

async def setup(bot):
    await bot.add_cog(MessageDeletionCog(bot))
