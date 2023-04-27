from src.core.bot import Bot

from .about import About


def setup(bot: Bot) -> None:
    bot.add_cog(About(bot))
