from typing import Optional

from disnake import Message
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import Message as MessageModel
from src.core.database import User as UserModel
from src.utils import CONFIG


class OnMessage(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.guild:
            return

        if message.author.bot:
            return

        if message.guild.id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Messsage event queued.")

        await self.bot.sync_completed.wait()

        if not await UserModel.objects.get(id=message.author.id):
            return

        thread_id: Optional[int] = None
        if message.thread:
            thread_id = message.thread.id

        await MessageModel.objects.create(
            id=message.id,
            created_at=message.created_at.replace(tzinfo=None),
            deleted=False,
            author=message.author.id,
            channel=message.channel.id,
            thread=thread_id,
        )
        logger.trace("Inserted message into the database.")
