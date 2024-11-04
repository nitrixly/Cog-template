import discord
import os
from discord.ext import commands
from core.config import TOKEN, OWNER, PREFIX

class CogModule(commands.AutoShardedBot):
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

client = CogModule()
client.run(TOKEN)
