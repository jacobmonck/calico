from datetime import datetime, timedelta
from textwrap import dedent

from disnake import Embed
from disnake.ext.commands import Cog, Context, command, has_guild_permissions
from humanize import precisedelta

from src import __version__
from src.core.bot import Bot, Context


class About(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command()
    @has_guild_permissions(administrator=True)
    async def about(self, ctx: Context) -> None:
        embed = Embed(
            title="About Calico",
            description=dedent(
                "Calico is an advanced metrics collection and processing tool for Dis"
                + "scord servers. It originally was developed for a community called "
                + "[GTA Online](https://discord.gg/gtao) and was used to collect "
                + "informative information about the community. Eventually it was "
                + "made open source (with a few changes and added features)."
            ),
        )

        uptime_delta = timedelta(seconds=0)
        if self.bot.online_since:
            uptime_delta = datetime.utcnow() - self.bot.online_since
        humanized_uptime = precisedelta(uptime_delta, format="%0.0f")

        ws_latency = round(self.bot.latency, 2) * 1000

        embed.add_field("Version", f"`{__version__}`")
        embed.add_field("Uptime", f"`{humanized_uptime}`")
        embed.add_field("Websocket Latency", f"`{ws_latency}`")

        await ctx.reply(embed=embed)
