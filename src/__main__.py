from sys import stderr
from os import environ

from disnake import Intents
from loguru import logger

from src.core.bot import Bot
from src.utils import CONFIG


def main() -> None:
    logger.remove()
    level=CONFIG.python.log_level.upper()
    logger.add(stderr, level=level)
    logger.add("logs/file_{time}.log", level="TRACE")

    bot = Bot(
        command_prefix=CONFIG.bot.prefix,
        intents=Intents.all(),
    )

    for ext in [
        "src.exts.commands",
        "src.exts.utils",
        "src.exts.listeners",
    ]:
        bot.load_extension(ext)

    bot.run(environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
