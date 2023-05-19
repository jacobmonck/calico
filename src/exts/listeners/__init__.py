from src.core.bot import Bot

from .members import OnMemberJoin, OnMemberRemove, OnMemberUpdate
from .messages import OnBulkMessageDelete, OnMessage, OnMessageDelete
from .reactions import (
    OnRawReactionAdd,
    OnRawReactionClear,
    OnRawReactionClearEmoji,
    OnRawReactionRemove,
)


def setup(bot: Bot) -> None:
    bot.add_cog(OnMessage(bot))
    bot.add_cog(OnMessageDelete(bot))
    bot.add_cog(OnBulkMessageDelete(bot))

    bot.add_cog(OnMemberJoin(bot))
    bot.add_cog(OnMemberUpdate(bot))
    bot.add_cog(OnMemberRemove(bot))

    bot.add_cog(OnRawReactionAdd(bot))
    bot.add_cog(OnRawReactionClear(bot))
    bot.add_cog(OnRawReactionRemove(bot))
    bot.add_cog(OnRawReactionClearEmoji(bot))
