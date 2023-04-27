from src.core.bot import Bot

from .on_bulk_message_delete import OnBulkMessageDelete
from .on_message import OnMessage
from .on_message_delete import OnMessageDelete


def setup(bot: Bot) -> None:
    bot.add_cog(OnMessage(bot))
    bot.add_cog(OnMessageDelete(bot))
    bot.add_cog(OnBulkMessageDelete(bot))
