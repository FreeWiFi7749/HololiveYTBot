import discord
from discord.ext import commands
import json

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = {
            "hello": "Hello, world!",
            "python": "Python is awesome!",
            # Add more tags and messages here
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content.lower()

        # Check if the message content is a tag
        if content in self.tags:
            tag = self.tags[content]
            await message.channel.send(tag)

    @commands.hybrid_group(name="tags", invoke_without_command=True)
    async def tags(self, ctx):
        """タグに関するコマンドを実行するにぇ"""
        await ctx.send("tags add <trigger> <message>\ntag remove <trigger>\ntag list")

    @tags.command(name="add")
    async def addtag(self, ctx, trigger, message):
        """Tagsを追加するにぇ"""
        self.tags[trigger.lower()] = message
        await ctx.send(f"Tag '{trigger}' added successfully!")
        save_tags_to_file()

    @tags.command(name="remove")
    async def removetag(self, ctx, trigger):
        """設定されているTagsを削除するにぇ"""
        if trigger.lower() in self.tags:
            del self.tags[trigger.lower()]
            await ctx.send(f"Tag '{trigger}' removed successfully!")
            save_tags_to_file()
        else:
            await ctx.send(f"Tag '{trigger}' does not exist!")

    @tags.command(name="list")
    async def listtags(self, ctx):
        """設定されているTagsのリストを表示するにぇ"""
        tags = "\n".join(self.tags.keys())
        await ctx.send(f"Tags:\n {tags}")

    def save_tags_to_file(self):
        with open("data/tags.json", 'w', encoding='utf-8') as file:
            json.dump(self.tags, file)

    def load_tags_from_file(self):
        try:
            with open("data/tags.json", 'r', encoding='utf-8') as file:
                self.tags = json.load(file)
        except FileNotFoundError:
            # If the file is not found, create an empty tags dictionary
            self.tags = {}

            with open("data/tags.json", 'r') as file:
                self.tags = json.load(file)
        except FileNotFoundError:
            # If the file is not found, create an empty tags dictionary
            self.tags = {}

    load_tags_from_file()

async def setup(bot):
    await bot.add_cog(Tags(bot))