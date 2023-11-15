import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

description = """An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here."""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="?", description=description, intents=intents)


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
