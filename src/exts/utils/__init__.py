from src.core.bot import Bot

from .sync import GuildSync


def setup(bot: Bot) -> None:
    bot.add_cog(GuildSync(bot))
