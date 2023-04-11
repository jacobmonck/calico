from os import environ

from disnake import Intents

from src.core.bot import Bot
from src.utils import CONFIG


def main() -> None:
    bot = Bot(
        command_prefix=CONFIG.bot.prefix,
        intents=Intents.all(),
    )

    for ext in ["src.exts.commands"]:
        bot.load_extension(ext)

    bot.run(environ["DISCORD_TOKEN"])


if __name__ == "__main__":
    main()
