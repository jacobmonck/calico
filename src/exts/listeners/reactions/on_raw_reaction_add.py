from datetime import datetime

from asyncpg import ForeignKeyViolationError
from disnake import RawReactionActionEvent
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Reaction as ReactionModel
from src.utils import CONFIG


class OnRawReactionAdd(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        if not payload.guild_id:
            return

        if not payload.member:
            return

        if payload.member.bot:
            return

        if payload.guild_id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Reaction add event queued.")

        await self.bot.sync_completed.wait()

        try:
            await ReactionModel.objects.create(
                name=payload.emoji.name,
                image_url=payload.emoji.url,
                added_at=datetime.utcnow().replace(tzinfo=None),
                removed=False,
                message=payload.message_id,
                user=payload.member.id,
            )
            logger.trace("Reaction added.")
        except ForeignKeyViolationError:
            return
