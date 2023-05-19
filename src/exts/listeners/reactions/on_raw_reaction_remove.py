from datetime import datetime

from asyncpg import ForeignKeyViolationError
from disnake import RawReactionActionEvent
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Reaction as ReactionModel
from src.utils import CONFIG


class OnRawReactionRemove(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        if not payload.guild_id:
            return

        if payload.guild_id != CONFIG.bot.guild_id:
            print("guild")
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Reaction remove event queued.")

        await self.bot.sync_completed.wait()

        reaction = await ReactionModel.objects.filter(
            message=payload.message_id, user=payload.user_id
        ).update(removed=True)

        if reaction == 0:
            return

        logger.trace("Reaction removed.")
