import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import pathlib

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
command_prefix = ['h/']

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = False
        self.cog_classes = {}

    async def on_ready(self):
        if not self.initialized:
            await self.change_presence(activity=discord.Game(name="起動中.."))
            print('------')
            print(f'Bot Username: {self.user.name}')
            print(f'BotID: {self.user.id}')
            print('------')
            await self.load_cogs()
            await self.load_log_cogs()
            await self.load_homepages_cogs()
            await bot.tree.sync()
            await self.change_presence(activity=discord.Game(name="にゃっはろ〜🌸"))
            self.initialized = True
            print('------')
            print('All cogs have been loaded and bot is ready.')
            print('------')
        else:
            print('Bot is already initialized.')

    async def load_cogs(self):
        folder_name = 'cogs'
        cur = pathlib.Path('.')
        for p in cur.glob(f"{folder_name}/*.py"):
            try:
                cog_name = f'cogs.{p.stem}'
                await self.load_extension(cog_name)
                print(f'{cog_name} loaded successfully.')
            except commands.ExtensionFailed as e:
                print(f'Failed to load extension {p.stem}: {e}')

    async def load_log_cogs(self):
        folder_name = 'cogs/log'
        cur = pathlib.Path('.')
        for p in cur.glob(f"{folder_name}/*.py"):
            try:
                cog_name = f'cogs.log.{p.stem}'
                await self.load_extension(cog_name)
                print(f'{cog_name} loaded successfully.')
            except commands.ExtensionFailed as e:
                print(f'Failed to load extension {p.stem}: {e}')

    async def load_homepages_cogs(self):
        folder_name = 'cogs/homepages'
        cur = pathlib.Path('.')
        for p in cur.glob(f"{folder_name}/*.py"):
            try:
                cog_name = f'cogs.homepages.{p.stem}'
                await self.load_extension(cog_name)
                print(f'{cog_name} loaded successfully.')
            except commands.ExtensionFailed as e:
                print(f'Failed to load extension {p.stem}: {e}')

intent: discord.Intents = discord.Intents.all()
bot = MyBot(command_prefix=command_prefix, intents=intent, help_command=None)

bot.run(TOKEN)
