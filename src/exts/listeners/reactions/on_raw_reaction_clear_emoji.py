from disnake import RawReactionClearEmojiEvent
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Reaction as ReactionModel
from src.utils import CONFIG


class OnRawReactionClearEmoji(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_clear_emoji(
        self, payload: RawReactionClearEmojiEvent
    ) -> None:
        if not payload.guild_id:
            return

        if payload.guild_id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Reaction emoji clear event queued.")

        await self.bot.sync_completed.wait()

        reactions = await ReactionModel.objects.filter(
            name=payload.emoji.name, message=payload.message_id
        ).update(removed=True)

        logger.trace(f"{reactions} reactions cleared.")
