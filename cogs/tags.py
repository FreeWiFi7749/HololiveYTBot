import discord
from discord.ext import commands
import json
from pathlib import Path

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tags = self.load_tags()

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
        await ctx.send("コマンド一覧はこちらだにぇ\n`h/tags add <trigger> <message>`\n`h/tag remove <trigger>`\n`h/tag list`")

    @tags.command(name="add")
    async def add_tag(self, ctx, trigger, *, message):
        """Tagsを追加するにぇ"""
        self.tags[trigger.lower()] = message
        await ctx.send(f"'{trigger}'を追加したにぇ！")
        self.save_tags()

    @tags.command(name="remove")
    async def removetag(self, ctx, trigger):
        """設定されているTagsを削除するにぇ"""
        if trigger.lower() in self.tags:
            del self.tags[trigger.lower()]
            await ctx.send(f"'{trigger}'を削除したにぇ！")
            self.save_tags()
        else:
            await ctx.send(f"'{trigger}'は存在しませんにぇ...")

    @tags.command(name="list")
    async def listtags(self, ctx):
        """設定されているTagsのリストを表示するにぇ"""
        tags = "\n".join(self.tags.keys())
        embed = discord.Embed(title="Tags", description=tags, color=discord.Color.blue())
        await ctx.send(embed=embed)

    def load_tags(self):
        path = Path('data/tags.json')
        if path.is_file():
            with path.open('r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}

    def save_tags(self):
        path = Path('data/tags.json')
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.tags, f, ensure_ascii=False, indent=4)

async def setup(bot):
    await bot.add_cog(Tags(bot))