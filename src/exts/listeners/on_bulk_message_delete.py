from disnake import RawBulkMessageDeleteEvent
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Message as MessageModel
from src.utils import CONFIG


class OnBulkMessageDelete(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_bulk_raw_message_delete(
        self, event: RawBulkMessageDeleteEvent
    ) -> None:
        if event.guild_id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Messsage delete event queued.")

        await self.bot.sync_completed.wait()

        for message_id in event.message_ids:
            if db_message := await MessageModel.objects.get_or_none(id=message_id):
                await db_message.update(deleted=True)
                logger.trace("Marked message as deleted in the database.")
