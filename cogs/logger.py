import discord
from discord.ext import commands
import os
from ._db import db, set_log_channel, update_log_channel, check_if_log_channel_exists


class Logger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(
        name="logger", description="Logger commands.", invoke_without_command=True
    )
    async def log(self, ctx: commands.Context):
        await ctx.send_help(ctx.command)

    @log.command(name="add", description="Add a logger to the server.")
    async def log_add(self, ctx: commands.Context, channel: discord.TextChannel):
        if check_if_log_channel_exists(ctx.guild.id):
            await ctx.send(
                "Logger already set up in this server, use `?logger update` to update the channel."
            )
            return
        set_log_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Logger set up in {channel.mention}!")

    @log.command(name="update", description="Update the logger channel.")
    async def log_update(self, ctx: commands.Context, channel: discord.TextChannel):
        if not check_if_log_channel_exists(ctx.guild.id):
            await ctx.send(
                "Logger not set up in this server, use `?logger add` to add the logger."
            )
            return
        update_log_channel(ctx.guild.id, channel.id)
        await ctx.send(f"Logger updated to {channel.mention}!")

    @log.command(name="remove", description="Remove the logger.")
    async def log_remove(self, ctx: commands.Context):
        if not check_if_log_channel_exists(ctx.guild.id):
            await ctx.send(
                "Logger not set up in this server, use `?logger add` to add the logger."
            )
            return
        db().table("logger").delete().eq("guild_id", ctx.guild.id).execute()
        await ctx.send("Logger removed!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Logger(bot))
    print("--> Logger cog loaded.")
