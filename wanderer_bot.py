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
    datetime.time(hour=5, minute=1, tzinfo=utc),
    datetime.time(hour=11, minute=1, tzinfo=utc),
    datetime.time(hour=17, minute=1, tzinfo=utc),
    datetime.time(hour=23, minute=1, tzinfo=utc),
]


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.check_vendors = True
        self.check_rapport = True

        self.reset_stock.start()
        self.update_stock.start()

    @tasks.loop(minutes=30)
    async def update_stock(self):
        if not self.check_vendors:
            return

        self.stock = merchant_scraper.scrape()
        
        legendary_card_stock = self.stock["legendary"]
        epic_card_stock = self.stock["epic"]
        rare_card_stock = self.stock["rare"]

        legendary_rapport_stock = self.stock["legendary_rapport"]
        epic_rapport_stock = self.stock["epic_rapport"]

        expiration = epoch_calc.get_epoch()
        channel = self.get_channel(channel_id)

        if legendary_card_stock or epic_card_stock or rare_card_stock:
            self.check_vendors = False
            legendary_card_str = ""
            epic_card_str = ""
            rare_card_str = ""            
            rapport_count = ""

            if legendary_card_stock:
                legendary_card_str = ", ".join(legendary_card_stock)
            if epic_card_stock:
                epic_card_str = ", ".join(epic_card_stock)
            if rare_card_stock:
                rare_card_str = ", ".join(rare_card_stock)

            stock_str = "```ansi\n"
            if len(legendary_card_str):
                stock_str += "[0;33m" + legendary_card_str + "[0;0m\n"
            if len(epic_card_str):
                stock_str += "[0;35m" + epic_card_str + "[0;0m\n"
            if len(rare_card_str):
                stock_str += "[0;34m" + rare_card_str + "[0;0m\n"

            stock_str += "```"

            if legendary_rapport_stock:
                rapport_count = f"\nLegendary Rapport: {len(legendary_rapport_stock)}\nEpic Rapport: {len(epic_rapport_stock)}\n"

            await channel.send(
                f"{mention_role}{stock_str}{rapport_count}Available until <t:{expiration}:t>"
            )

        elif legendary_rapport_stock and self.check_rapport:
            self.check_rapport = False
            rapport_count = f"\nLegendary Rapport: {len(legendary_rapport_stock)}\nEpic Rapport: {len(epic_rapport_stock)}\n"

            await channel.send(
                f"{mention_role}\nNo Cards Available at the moment{rapport_count}Available until <t:{expiration}:t>"
            )


    @update_stock.before_loop
    async def before_update_stock(self):
        await self.wait_until_ready()

    @tasks.loop(time=times)
    async def reset_stock(self):
        self.check_vendors = True
        self.check_rapport = True

    @reset_stock.before_loop
    async def before_reset_vendors(self):
        await self.wait_until_ready()


bot = Bot()
bot.run(discord_token)
