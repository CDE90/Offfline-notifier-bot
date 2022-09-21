import json

import aiohttp
import discord
import requests
from discord.ext import commands, tasks

import config
from bot import OfflineBot

with open("data/bots.json", "r") as f:
    bots = json.load(f)


class OfflineChecker(commands.Cog):
    def __init__(self, client: OfflineBot):
        self.client = client
        self.check_offline.start()

    async def notify(self, bot: str, online: bool):
        print(f"{bot} is now {'online' if online else 'offline'}")

        message = "{} is now {}".format(
            bot, "online. :tada:" if online else "offline. :sob:"
        )

        async with aiohttp.ClientSession() as session:
            for hook_url in config.WEBHOOK_URLS:
                webhook = discord.Webhook.from_url(hook_url, session=session)
                await webhook.send(message, username="Offline Notification")

        channel = self.client.get_channel(config.NOTIFICATION_CHANNEL)
        if not isinstance(channel, discord.TextChannel):
            return
        await channel.send(f"{message}\n<@652797071623192576> <@602235481459261440>")

    @tasks.loop(seconds=5)
    async def check_offline(self):
        for bot in bots:
            try:
                response = requests.request(
                    "GET", f"http://{bots[bot]['address']}:{bots[bot]['port']}/status"
                )
            except requests.exceptions.ConnectionError:
                response = None

            if not response:
                before_status = bots[bot]["online"]

                if before_status == False:
                    return

                with open("data/bots.json", "w") as f:
                    bots[bot]["online"] = False
                    json.dump(bots, f, indent=4)

                await self.notify(bot, False)

            elif response.status_code == 200:

                before_status = bots[bot]["online"]

                if before_status == True:
                    return

                with open("data/bots.json", "w") as f:
                    bots[bot]["online"] = True
                    json.dump(bots, f, indent=4)

                await self.notify(bot, True)

    @check_offline.before_loop
    async def before_check_offline(self):
        await self.client.wait_until_ready()


async def setup(client: OfflineBot):
    await client.add_cog(OfflineChecker(client))
