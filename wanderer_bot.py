#!/usr/bin/env python3
import os
import datetime
from nextcord.ext import tasks, commands
from dotenv import load_dotenv
import merchant_scraper
import epoch_calc

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))
role_id = os.getenv("ROLE_ID")
mention_role = f"<@&{role_id}>"
utc = datetime.timezone.utc

times = [
    datetime.time(hour=5, tzinfo=utc),
    datetime.time(hour=11, tzinfo=utc),
    datetime.time(hour=17, tzinfo=utc),
    datetime.time(hour=23, tzinfo=utc),
]


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_vendors = True

        self.reset_stock.start()
        self.update_stock.start()

    @tasks.loop(minutes=30)
    async def update_stock(self):
        if not self.check_vendors:
            return

        self.stock = merchant_scraper.scrape()
        print(self.stock)
        print(len(self.stock["Rare"]))

        if self.stock["Legendary"] or self.stock["Epic"] or self.stock["Rare"]:
            self.check_vendors = False
            channel = self.get_channel(channel_id)
            legendary_stock = ""
            epic_stock = ""
            rare_stock = ""

            if self.stock["Legendary"]:
                legendary_stock = ", ".join(self.stock["Legendary"])
            if self.stock["Epic"]:
                epic_stock = ", ".join(self.stock["Epic"])
            if self.stock["Rare"]:
                rare_stock = ", ".join(self.stock["Rare"])

            stock_str = "```ansi\n"
            if len(legendary_stock):
                stock_str += legendary_stock + "\n"
            if len(epic_stock):
                stock_str += epic_stock + "\n"
            if len(rare_stock):
                stock_str += rare_stock + "\n"

            stock_str += "```"
            print(stock_str)
            expiration = epoch_calc.get_epoch()

            await channel.send(
                f"{mention_role}{stock_str}Available until <t:{expiration}:t>"
            )

    @update_stock.before_loop
    async def before_update_stock(self):
        await self.wait_until_ready()

    @tasks.loop(time=times)
    async def reset_stock(self):
        self.check_vendors = True

    @reset_stock.before_loop
    async def before_reset_vendors(self):
        await self.wait_until_ready()


bot = Bot()
bot.run(discord_token)
