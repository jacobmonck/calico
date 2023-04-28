from src.core.bot import Bot

from .members import OnMemberJoin, OnMemberRemove, OnMemberUpdate
from .messages import OnBulkMessageDelete, OnMessage, OnMessageDelete


def setup(bot: Bot) -> None:
    bot.add_cog(OnMessage(bot))
    bot.add_cog(OnMessageDelete(bot))
    bot.add_cog(OnBulkMessageDelete(bot))

    bot.add_cog(OnMemberJoin(bot))
    bot.add_cog(OnMemberUpdate(bot))
    bot.add_cog(OnMemberRemove(bot))
