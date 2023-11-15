import discord
from discord.embeds import Embed

def create_embed(
    member: discord.Member,
    title: str,
    reason: int,
    channel: discord.TextChannel,
    message: discord.Message,
    malicious_file_url: str = None,
) -> discord.Embed:
    description = f"Message from **{member.mention}** was removed from {channel.mention} for containing malicious {'link(s)' if reason == 1 else 'file(s)'}!\n\n**Message Content:**\n{message.content}"
    if malicious_file_url:
        description += f"\n\n**Malicious File's URL:**\n{malicious_file_url}"
    embed = Embed(
        colour=discord.Colour.random(),
        title=title,
        description=description,
        timestamp=discord.utils.utcnow(),
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(
        text=f"Member ID: {member.id} | Message ID: {message.id}",
        icon_url=member.avatar.url,
    )

    return embed
