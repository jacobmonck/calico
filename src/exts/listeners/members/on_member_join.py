from disnake import Member
from disnake.ext.commands import Cog
from loguru import logger
from orjson import dumps

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

        joined_at = None
        if member.joined_at:
            joined_at = member.joined_at.replace(tzinfo=None)

        if db_user := await UserModel.objects.get_or_none(member.id):
            await db_user.update(
                username=member.name,
                nickname=member.nick,
                discriminator=int(member.discriminator),
                avatar_hash=getattr(member.avatar, "key", None),
                guild_avatar_hash=getattr(member.guild_avatar, "key", None),
                created_at=member.created_at.replace(tzinfo=None),
                joined_at=joined_at,
                in_guild=True,
                pending=member.pending,
                flags=dumps(dict(member.flags)).decode(),
            )
        else:
            await UserModel.objects.create(
                id=member.id,
                username=member.name,
                nickname=member.nick,
                discriminator=int(member.discriminator),
                avatar_hash=getattr(member.avatar, "key", None),
                guild_avatar_hash=getattr(member.guild_avatar, "key", None),
                created_at=member.created_at.replace(tzinfo=None),
                joined_at=joined_at,
                in_guild=True,
                pending=member.pending,
                flags=dumps(dict(member.flags)).decode(),
            )
        logger.trace("Member added to the database.")
