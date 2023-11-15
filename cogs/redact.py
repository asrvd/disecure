import discord
from discord.ext import commands
from pangea.services import Redact
import os
from dotenv import load_dotenv
import re

url_regex = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    # domain...
    r"(?:\S+(?::\S*)?@)?"  # optional user:pass
    r"(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
    r"(?:[a-z0-9-]*[a-z0-9])"
    r"|"  # OR ip address...
    r"(?:"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)"  # 0-255
    r"(?:\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)){3}"
    r")"
    r")"
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)

load_dotenv()

redact = Redact(token=os.getenv("REDACT_TOKEN"))


class Redact(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        for word in message.content.split():
            if url_regex.match(word):
                return

        response = redact.redact(message.content)

        if response.status.lower() == "success" and response.result.count > 0:
            await message.delete()
            await message.channel.send(
                f"1 message redacted from {message.author.mention}, redacted message: {response.result.redacted_text}",
                delete_after=5,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Redact(bot))
    print("--> Redact cog loaded.")
