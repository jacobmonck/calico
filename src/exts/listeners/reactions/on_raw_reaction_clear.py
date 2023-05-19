from disnake import RawReactionClearEvent
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Reaction as ReactionModel
from src.utils import CONFIG


class OnRawReactionClear(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_clear(self, payload: RawReactionClearEvent) -> None:
        if not payload.guild_id:
            return

        if payload.guild_id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Reaction clear event queued.")

        await self.bot.sync_completed.wait()

        reactions = await ReactionModel.objects.filter(
            message=payload.message_id
        ).update(removed=True)

        logger.trace(f"{reactions} reactions marked as removed.")
