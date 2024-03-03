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
        self.ready_check = False
        super().__init__(*args, **kwargs)

    async def setup_hook(self):
        if not self.ready_check:
            print('------')
            print(f'Bot Username: {self.user.name}')
            print(f'BotID: {self.user.id}')
            print('------')
            folder_name = 'cogs'
            cur = pathlib.Path('.')

            for p in cur.glob(f"{folder_name}/*.py"):

                try:
                    print(f'cogs.{p.stem}', end="　")
                    await bot.load_extension(f'cogs.{p.stem}')
                    print(f'success')

                except commands.errors.NoEntryPointError:
                    print(f'module.{p.stem}')

            self.ready_check = True

        else:
            print('The start up process is already complete!')


intent: discord.Intents = discord.Intents.all()
bot = MyBot(command_prefix=command_prefix, intents=intent)

bot.run(TOKEN)
