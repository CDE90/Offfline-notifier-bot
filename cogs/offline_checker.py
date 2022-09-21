import json

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

                print(f"{bot} is now offline!")

                channel = self.client.get_channel(config.NOTIFICATION_CHANNEL)
                if not isinstance(channel, discord.TextChannel):
                    return
                await channel.send(
                    f"{bot} is now offline! :sob:\n<@652797071623192576> <@602235481459261440>"
                )

            elif response.status_code == 200:

                before_status = bots[bot]["online"]

                if before_status == True:
                    return

                with open("data/bots.json", "w") as f:
                    bots[bot]["online"] = True
                    json.dump(bots, f, indent=4)

                print(f"{bot} is now online!")

                channel = self.client.get_channel(config.NOTIFICATION_CHANNEL)

                if not isinstance(channel, discord.TextChannel):
                    return
                await channel.send(
                    f"{bot} is now online! :tada:\n<@652797071623192576><@602235481459261440>"
                )

    @check_offline.before_loop
    async def before_check_offline(self):
        await self.client.wait_until_ready()


async def setup(client: OfflineBot):
    await client.add_cog(OfflineChecker(client))
