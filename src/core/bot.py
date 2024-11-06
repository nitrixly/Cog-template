import os
import discord
from discord.ext import commands
from utils.logger import logger
from prisma import Prisma
import utils.config
from typing import List, Callable, Coroutine

intents = discord.Intents.default()
intents.message_content = True
intents.member = True
intents.presence = True

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix="?",
            intents=intents,
            activity=discord.Activity(type=discord.ActivityType.playing, name="Papa"),
            status=discord.Status.dnd,
            owner_ids=utils.config.OWNER_IDS
        )
        self.database = None
        self.startup_tasks: List[Callable[["Bot"], Coroutine]] = []

    @property
    def db(self) -> Prisma:
        return self.database

    def add_startup_task(self, task: Callable[["Bot"], Coroutine]):
        self.startup_tasks.append(task)

    async def load_cogs(self):
        cogs_dir = "./src/cogs"
        for root, _, files in os.walk(cogs_dir):
            for file in files:
                if file.endswith(".py"):
                    cog = os.path.join(root, file).replace(cogs_dir, '').replace(os.sep, '.').rstrip('.py')
                    try:
                        await self.load_extension(cog)
                        logger.info(f"Loaded cog {cog}")
                    except Exception as e:
                        logger.error(f"Failed to load {cog}: {e}")
        await self.load_extension("jishaku")

    async def connect_database(self):
        self.database = Prisma()
        try:
            await self.database.connect()
            logger.info("Database connected.")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")

    async def setup_hook(self):
        await self.tree.sync()
        for task in self.startup_tasks:
            await task(self)

    async def close(self):
        if self.db and self.db.is_connected:
            await self.db.disconnect()
            logger.info("Database disconnected.")
        await super().close()

    async def on_ready(self):
        logger.info(f"Bot is ready and logged in as {self.user}")

bot = Bot()
bot.add_startup_task(bot.load_cogs)
bot.add_startup_task(bot.connect_database)

if __name__ == "__main__":
    bot.run(utils.config.BOT_TOKEN)
