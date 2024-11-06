import discord
import os
from discord.ext import commands
from settings.config import TOKEN, OWNER, PREFIX

class Aether(commands.Shard):
    def __init__(self):
        super().__init__(command_prefix=PREFIX, intents=discord.Intents.all(), shard_count=1)
        self.owner_ids = OWNER

    async def on_ready(self):
        print(f"{self.user.name} is ready!")

    async def setup_hook(self):
        await self.load_extension('jishaku')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f'[Loaded] `{filename}`')
                except Exception as e:
                    print(f'Failed to load {filename}: {e}')
        await self.tree.sync()

client = Aether()
client.run(TOKEN)
