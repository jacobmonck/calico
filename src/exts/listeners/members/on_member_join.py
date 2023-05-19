from disnake import Member
from disnake.ext.commands import Cog
from loguru import logger

from src.core.bot import Bot
from src.core.database import User as UserModel
from src.utils import CONFIG


class OnMemberJoin(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member: Member) -> None:
        if member.guild.id != CONFIG.bot.guild_id:
            return

        if not self.bot.sync_completed.is_set():
            logger.trace("Member join event queued.")

        await self.bot.sync_completed.wait()

        await UserModel.upsert_member(member)
