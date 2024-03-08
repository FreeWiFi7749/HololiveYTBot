import discord
from discord.ext import commands
import json
import os

class ConfigSelectView(discord.ui.View):
    def __init__(self, bot, ctx, mode, channels_data=None):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.mode = mode

        if mode == "add" and channels_data:
            options = [
                discord.SelectOption(label=channel["name"], value=channel["channel_id"])
                for channel in channels_data
            ]
        else:
            config = self.ctx.cog.load_config(ctx.guild.id)
            options = [
                discord.SelectOption(label=f"設定 #{idx + 1}", description=f"{self.bot.get_channel(int(c['source_channel_id'])).name}", value=str(idx))
                for idx, c in enumerate(config)
            ]

        self.add_item(ConfigSelectMenu(options=options, custom_id="select_menu", mode=mode))

class ConfigSelectMenu(discord.ui.Select):
    def __init__(self, options, custom_id, mode):
        super().__init__(placeholder="選択してください...", options=options, custom_id=custom_id)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):
        selected_index = int(self.values[0])
        if self.mode == "remove":
            self.view.ctx.cog.remove_config(interaction.guild.id, selected_index)
            await interaction.response.send_message(f"設定 #{selected_index + 1} を削除しました。", ephemeral=True)
        elif self.mode == "add":
            new_config = {
                "source_channel_id": self.values[0],
                "target_channel_id": str(interaction.channel_id)
            }
            self.view.ctx.cog.update_or_add_config(interaction.guild.id, new_config)
            await interaction.response.send_message(f"ソースチャンネルを {self.values[0]} に設定しました。", ephemeral=True)
            await interaction.message.delete()
            await interaction.followup.send("ロールを選択してください\n設定しなくてもいい場合はこのメッセージを消去してください:", view=ConfigRoleSelectView(self.view.bot, self.view.ctx, self.values[0], str(interaction.channel_id)), ephemeral=True)

class ConfigRoleSelectView(discord.ui.View):
    def __init__(self, bot, ctx, source_channel_id, target_channel_id):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.source_channel_id = source_channel_id
        self.target_channel_id = target_channel_id

        options = [
            discord.SelectOption(label=role.name, value=str(role.id))
            for role in ctx.guild.roles
        ]
        if len(options) > 25:
            option_lists = [options[i:i+25] for i in range(0, len(options), 25)]
            for i, option_list in enumerate(option_lists):
                self.add_item(ConfigRoleSelectMenu(options=option_list, custom_id=f"select_role_menu_{source_channel_id}_{target_channel_id}_{i}"))
        else:
            self.add_item(ConfigRoleSelectMenu(options=options, custom_id=f"select_role_menu_{source_channel_id}_{target_channel_id}"))

class ConfigRoleSelectMenu(discord.ui.Select):
    async def callback(self, interaction: discord.Interaction):
        new_config = {
            "mention_role_id": self.values[0]
        }
        self.view.ctx.cog.update_or_add_config(interaction.guild.id, new_config)
        await interaction.response.send_message("ロールを設定したにぇ", ephemeral=True)
        await interaction.followup.send("Twitter転送設定が完了したにぇ", ephemeral=True)

class TwitterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_folder = 'data/twitter_forward'
        if not os.path.exists(self.config_folder):
            os.makedirs(self.config_folder)

    def config_path(self, guild_id):
        return os.path.join(self.config_folder, f'{guild_id}.json')

    def load_config(self, guild_id):
        try:
            with open(self.config_path(guild_id), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def update_or_add_config(self, guild_id, new_config):
        configs = self.load_config(guild_id)
        updated = False
        for config in configs:
            if config["source_channel_id"] == new_config["source_channel_id"]:
                config.update(new_config)
                updated = True
                break
        if not updated:
            configs.append(new_config)
        
        self.save_config(guild_id, configs)

    def save_config(self, guild_id, configs):
        with open(self.config_path(guild_id), 'w') as f:
            json.dump(configs, f, ensure_ascii=False, indent=4)

    def remove_config(self, guild_id, index):
        config = self.load_config(guild_id)
        if config and 0 <= index < len(config):
            del config[index]
            self.save_config(guild_id, config)

    def load_all_configs(self):
        all_files = os.listdir(self.config_folder)
        all_configs = []
        for filename in all_files:
            if filename.endswith('.json'):
                path = os.path.join(self.config_folder, filename)
                with open(path, 'r') as f:
                    config = json.load(f)
                    all_configs.append(config)
        return all_configs

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('data/twitter_channels.json', 'r') as f:
            twitter_channels = json.load(f)["twitter_channels"]
    
        source_channel_info = next((c for c in twitter_channels if str(message.channel.id) == c["channel_id"]), None)
        if source_channel_info:
            guild_configs = self.load_all_configs()
            for guild_config in guild_configs:
                for config in guild_config:
                    if config["source_channel_id"] == source_channel_info["channel_id"]:
                        print("転送", config["source_channel_id"], config["target_channel_id"], message.content)
                        target_channel = self.bot.get_channel(int(config['target_channel_id']))
                    if target_channel:
                        role_mention = ""
                        if "mention_role_id" in config:
                            print("mention_role_id", config["mention_role_id"])
                            role = message.guild.get_role(int(config['mention_role_id']))
                            if role:
                                role_mention = role.mention

                        if message.webhook_id:
                            webhook_name = message.author.name.replace("• TweetShift", "")
                            webhook_icon_url = message.author.avatar_url
                            webhook = await target_channel.create_webhook(name=webhook_name)
                            try:
                                await webhook.send(content=f"{role_mention}\n{message.content}",
                                                   username=webhook_name, avatar_url=webhook_icon_url)
                                print("転送完了")
                            finally:
                                await webhook.delete()
                        else:
                            await target_channel.send(f"{role_mention} {message.content}")
                            print("転送完了")

    @commands.hybrid_group(name="twitter", with_app_command=True, invoke_without_command=True)
    async def twitter(self, ctx):
        await ctx.send("Twitter関連のコマンドだにぇ", ephemeral=True)

    @twitter.command(name="setup")
    async def setup(self, ctx, enable: bool = True):
        """Twitter転送機能を有効化するかどうかを設定するにぇ"""
        self.save_config(ctx.guild.id, [])
        message = "Twitter機能が有効になったにぇ" if enable else "Twitter機能が無効になったにぇ"
        await ctx.send(message, ephemeral=True)

    @twitter.command(name="list")
    async def list(self, ctx):
        """設定されている転送設定のリストを表示するにぇ"""
        config = self.load_config(ctx.guild.id)
        if not config:
            await ctx.send("現在設定されている転送は無いにぇ", ephemeral=True)
            return

        embed = discord.Embed(title="Twitter転送設定リスト", color=discord.Color.blue())
        for idx, setting in enumerate(config, start=1):
            source_channel = self.bot.get_channel(int(setting['source_channel_id']))
            target_channel = self.bot.get_channel(int(setting['target_channel_id']))
            role = ctx.guild.get_role(int(setting['mention_role_id'])) if 'mention_role_id' in setting else "なし"
            embed.add_field(name=f"設定 #{idx}", value=f"ソース: {source_channel.name if source_channel else '不明'}\nチャンネル: {target_channel.mention if target_channel else '不明'}\nロール: {role.mention if role else 'なし'}", inline=False)
        await ctx.send(embed=embed, ephemeral=True)

    @twitter.command(name="add")
    async def add(self, ctx):
        """Twitter転送設定を追加するにぇ"""
        await ctx.defer()
        with open('data/twitter_channels.json', 'r') as f:
            channels_data = json.load(f)["twitter_channels"]
        await ctx.send("ソースチャンネルを選択してください:", view=ConfigSelectView(self.bot, ctx, "add", channels_data), ephemeral=True)

    @twitter.command(name="remove")
    async def remove(self, ctx):
        """Twitter転送設定を削除するにぇ"""
        config = self.load_config(ctx.guild.id)
        if not config:
            await ctx.send("削除する設定がありません。", ephemeral=True)
            return
        await ctx.send("削除する設定を選択してください:", view=ConfigSelectView(self.bot, ctx, config, "remove"), ephemeral=True)

async def setup(bot):
    await bot.add_cog(TwitterCog(bot))
