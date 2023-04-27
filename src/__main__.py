import sys
from os import environ

from disnake import Intents
from loguru import logger

from src.core.bot import Bot
from src.utils import CONFIG


def main() -> None:
    bot = Bot(
        command_prefix=CONFIG.bot.prefix,
        intents=Intents.all(),
    )
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    for ext in [
        "src.exts.commands",
        "src.exts.utils",
    ]:
        bot.load_extension(ext)

    bot.run(environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
