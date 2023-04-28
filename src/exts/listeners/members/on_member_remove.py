from disnake import Member
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import User as UserModel
from src.utils import CONFIG


class OnMemberRemove(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_remove(self, member: Member) -> None:
        if member.guild.id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Member remove event queued.")

        await self.bot.sync_completed.wait()

        if db_user := await UserModel.objects.get_or_none(id=member.id):
            await db_user.update(in_guild=False)
            logger.trace("Member marked as not in guild.")
