import discord
from discord.ext import commands
import json
import os

class MemoView(discord.ui.View):
    def __init__(self, memos, user_id):
        super().__init__()
        self.memos = memos
        self.user_id = user_id
        self.current_index = 0

    @discord.ui.button(label="前へ", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_index > 0:
            self.current_index -= 1
            await interaction.response.edit_message(content="", embed=self.get_memo_embed())

    @discord.ui.button(label="次へ", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_index < len(self.memos) - 1:
            self.current_index += 1
            await interaction.response.edit_message(content="", embed=self.get_memo_embed())

    @discord.ui.button(label="閉じる", style=discord.ButtonStyle.danger)
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.delete()

    def get_memo_embed(self):
        embed = discord.Embed(title=f"メモ {self.current_index + 1}/{len(self.memos)}", description=self.memos[self.current_index], color=discord.Color.blue())
        return embed

class ToolsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="memo", invoke_without_command=True)
    async def memo_group(self, ctx):
        """メモに関するコマンドを実行するにぇ"""
        await ctx.send_help(ctx.command)

    @memo_group.command(name="add", description="メモを追加")
    async def add_memo(self, ctx, *, memo: str):
        """メモを追加するにぇ"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        memo_file = f'data/notes/{guild_id}_{user_id}.json'

        if not os.path.exists('data/notes'):
            os.makedirs('data/notes')

        if os.path.exists(memo_file):
            with open(memo_file, 'r', encoding='utf-8') as f:
                memos = json.load(f)
        else:
            memos = []

        memos.append(memo)

        with open(memo_file, 'w', encoding='utf-8') as f:
            json.dump(memos, f, ensure_ascii=False, indent=4)

        await ctx.send('メモを追加したにぇ', ephemeral=True)

    @memo_group.command(name="show")
    async def show_memos(self, ctx):
        """メモを表示するにぇ"""
        user_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        memo_file = f'data/notes/{guild_id}_{user_id}.json'

        if not os.path.exists(memo_file):
            await ctx.send('メモが見つからなかったにぇ...', ephemeral=True)
            return

        with open(memo_file, 'r', encoding='utf-8') as f:
            memos = json.load(f)

        if not memos:
            await ctx.send('メモがないみたいだにぇ', ephemeral=True)
            return

        view = MemoView(memos, user_id)
        await ctx.send(embed=view.get_memo_embed(), view=view)

async def setup(bot):
    await bot.add_cog(ToolsCog(bot))
