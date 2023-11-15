import discord
from discord.ext import commands
from pangea.services import FileScan
from pangea.config import PangeaConfig
from pangea.tools import logger_set_pangea_config
import os
from dotenv import load_dotenv
from ._db import get_log_channel
from ._utils import create_embed

load_dotenv()

domain = os.getenv("PANGEA_DOMAIN")

fs_config = PangeaConfig(
    domain=domain, queued_retry_enabled=True, poll_result_timeout=120
)

fs = FileScan(token=os.getenv("FILESCAN_TOKEN"), config=fs_config, logger_name="fs")
logger_set_pangea_config(logger_name=fs.logger.name)


class AttachmentScan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        original_message = message
        if message.attachments:
            log_channel_id = get_log_channel(message.guild.id)
            msg = await message.reply(
                "Scanning file(s) in this message...", mention_author=False
            )
            await message.add_reaction("🔍")
            flag = False
            for attachment in message.attachments:
                await attachment.save(attachment.filename)
                with open(attachment.filename, "rb") as f:
                    response = fs.file_scan(file=f)

                    if response.result.data.verdict == "malicious":
                        await message.delete()
                        await message.channel.send(
                            f"1 message deleted from {message.author.mention} for containing malicious file(s), malicious file: {attachment.filename}",
                            delete_after=5,
                        )
                        flag = True
                        if log_channel_id:
                            log_channel = self.bot.get_channel(log_channel_id)
                            emb = create_embed(
                                member=message.author,
                                title="Malicious File(s) found & removed!",
                                reason=1,
                                channel=message.channel,
                                message=original_message,
                            )
                            await log_channel.send(
                                embed=emb,
                            )
                os.remove(attachment.filename)
                if flag:
                    break
            await msg.edit(
                content="File(s) scanned, no malicious files found.", delete_after=5
            )
            await message.remove_reaction("🔍", self.bot.user)
            await message.add_reaction("✅")


async def setup(bot: commands.Bot):
    await bot.add_cog(AttachmentScan(bot))
    print("--> File Scan cog loaded.")
