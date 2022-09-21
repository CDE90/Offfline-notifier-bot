import asyncio
import discord
from discord.ext import commands
import os
import config


class MyClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(">"), intents=discord.Intents.default())

    async def on_readu(self):
        print(f"Logged in as {self.user}")


client = MyClient()


@client.command()
async def pint(ctx: commands.Context):
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
