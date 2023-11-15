import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

description = """A simple Discord bot that keeps your server safe and secure using Pangea's API.

This bot is open source and the code can be found here: https://github.com/asrvd/disguard"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="p.", description=description, intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def setup_hook():
    await load_cogs()


@bot.event
async def on_ready():
    print(f"--> Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


bot.run(os.getenv("BOT_TOKEN"))
