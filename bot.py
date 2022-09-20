import discord
from discord.ext import commands
import os
import json
import asyncio
import config

with open("data/bots.json", "r") as f:
    bots = json.load(f)

class OfflineBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or(";"), intents=discord.Intents.all())

    async def on_ready(self):
        await self.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Offline Bots!"))

        print(f"Logged in as {self.user}")

client = OfflineBot()

@client.command()
async def ping(ctx: commands.Context):
    await ctx.send(f"Pong! {round(client.latency * 1000, 1)}ms")

async def main():
    async with client:
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename[:-3]}")
        await client.start(config.BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
