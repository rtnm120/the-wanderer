#!/usr/bin/env python3
import os
import datetime
from nextcord.ext import tasks, commands
from dotenv import load_dotenv
import merchant_scraper

load_dotenv()

discord_token = os.getenv("DISCORD_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))
mention_role = f"<@&{os.getenv("ROLE_ID")}>"
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

        if len(self.stock):
            channel = self.get_channel(channel_id)
            stock_str = ", ".join(self.stock)
            
            await channel.send(f"{mention_role}\nNew cards available:\n{stock_str}")

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
