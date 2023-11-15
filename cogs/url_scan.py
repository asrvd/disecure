import discord
from discord.ext import commands
from pangea.services import UrlIntel

import os
from ._db import get_log_channel
from dotenv import load_dotenv
import re
from ._utils import create_embed

load_dotenv()

us = UrlIntel(token=os.getenv("URLSCAN_TOKEN"))

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


class URLScan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        log_channel_id = get_log_channel(message.guild.id)
        if message.author == self.bot.user:
            return
        original_message = message
        for word in message.content.split():
            if url_regex.match(word):
                response = us.reputation(url=word)
                if response.result.data.verdict == "malicious":
                    await message.delete()
                    await message.channel.send(
                        f"1 message deleted from {message.author.mention} for containing malicious url(s)!",
                        delete_after=5,
                    )
                    if log_channel_id:
                        log_channel = self.bot.get_channel(log_channel_id)
                        emb = create_embed(
                            member=message.author,
                            title="Malicious URL found & removed!",
                            reason=1,
                            channel=message.channel,
                            message=original_message,
                        )
                        await log_channel.send(
                            embed=emb,
                        )
                    break


async def setup(bot: commands.Bot):
    await bot.add_cog(URLScan(bot))
    print("--> URL Scan cog loaded.")
