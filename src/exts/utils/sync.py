from time import perf_counter
from typing import Any, List

from disnake import Guild, TextChannel, Thread
from disnake.abc import GuildChannel
from disnake.ext.commands import Cog
from loguru import logger
from orjson import dumps

from src.core.bot import Bot
from src.core.database import Category as CategoryModel
from src.core.database import Channel as ChannelModel
from src.core.database import Thread as ThreadModel
from src.core.database import User as UserModel
from src.utils import CONFIG


def is_staff_channel(channel: TextChannel) -> bool:
    if channel.category:
        if channel.category_id in CONFIG.bot.staff_categories:
            return True

    if channel.id in CONFIG.bot.staff_channels:
        return True

    return False


class GuildSync(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def sync_members(self, guild: Guild) -> None:
        self.bot.sync_completed.clear()

        logger.info("Fetching guild members from the API, this could take a awhile...")
        start = perf_counter()

        await guild.chunk()

        time = "{:.2f}".format(perf_counter() - start)
        logger.info(f"Fetched members from the API in {time} seconds.")

        await UserModel.objects.update(each=True, in_guild=False)

        users: List[List[Any]] = []

        logger.info("Parsing member data, this could take a second...")
        for member in guild.members:
            joined_at = None
            if member.joined_at:
                joined_at = member.joined_at.replace(tzinfo=None)

            users.append(
                [
                    member.id,
                    member.name,
                    member.nick,
                    int(member.discriminator),
                    getattr(member.avatar, "key", None),
                    getattr(member.guild_avatar, "key", None),
                    member.created_at.replace(tzinfo=None),
                    joined_at,
                    True,
                    member.pending,
                    dumps(dict(member.flags)).decode(),
                ]
            )

        logger.info("Updating members in the database, this could take a awhile...")
        start = perf_counter()

        await UserModel.bulk_upsert(users)

        time = "{:.2f}".format(perf_counter() - start)
        logger.info(f"Updated a total of {len(users)} rows in {time} seconds.")

    async def sync_channels(self, guild: Guild) -> None:
        self.bot.sync_completed.clear()

        logger.info("synchronizing guild channels...")

        for category in guild.categories:
            if category.id in CONFIG.bot.ignored_categories:
                continue

            if db_category := await CategoryModel.objects.get_or_none(id=category.id):
                await db_category.update(
                    name=category.name,
                )
            else:
                await CategoryModel.objects.create(
                    id=category.id,
                    name=category.name,
                )

        logger.trace("Finished synchronizing guild categories.")

        for channel in guild.channels:
            if not isinstance(channel, TextChannel):
                continue

            if channel.category:
                if channel.category_id in CONFIG.bot.ignored_categories:
                    continue

            if channel.id in CONFIG.bot.ignored_channels:
                continue

            if db_channel := await ChannelModel.objects.get_or_none(id=channel.id):
                await db_channel.update(
                    name=channel.name,
                    staff=is_staff_channel(channel),
                    category=channel.category_id,
                )
            else:
                await ChannelModel.objects.create(
                    id=channel.id,
                    name=channel.name,
                    staff=is_staff_channel(channel),
                    category=channel.category_id,
                )

        logger.trace("Finished synchronizing guild channels.")

        for thread in guild.threads:
            if thread.parent and thread.parent.category:
                if thread.category_id in CONFIG.bot.ignored_categories:
                    continue

            if thread.parent_id in CONFIG.bot.ignored_channels:
                continue

            if db_thread := await ThreadModel.objects.get_or_none(id=thread.id):
                await db_thread.update(
                    name=thread.name,
                    created_at=thread.created_at.replace(tzinfo=None),
                    archived=thread.archived,
                    auto_archive_duration=thread.auto_archive_duration,
                    locked=thread.locked,
                    type=str(thread.type),
                )
            else:
                await ThreadModel.objects.create(
                    id=thread.id,
                    name=thread.name,
                    created_at=thread.created_at.replace(tzinfo=None),
                    archived=thread.archived,
                    auto_archive_duration=thread.auto_archive_duration,
                    locked=thread.locked,
                    type=str(thread.type),
                )

        logger.trace("Finished synchronizing guild threads.")

        logger.info("Finished synchonizing guild channels.")

        self.bot.sync_completed.set()

    @Cog.listener()
    async def on_guild_available(self, guild: Guild) -> None:
        if guild.id != CONFIG.bot.guild_id:
            return

        await self.sync_members(guild)
        await self.sync_channels(guild)

    @Cog.listener()
    async def on_guild_unavailable(self, guild: Guild) -> None:
        if guild.id != CONFIG.bot.guild_id:
            return

        self.bot.sync_completed.clear()

    @Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel) -> None:
        if channel.guild.id != CONFIG.bot.guild_id:
            return

        await self.sync_channels(channel.guild)

    @Cog.listener()
    async def on_guild_channel_update(
        self, _: GuildChannel, channel: GuildChannel
    ) -> None:
        if channel.guild.id != CONFIG.bot.guild_id:
            return

        await self.sync_channels(channel.guild)

    @Cog.listener()
    async def on_thread_channel_create(self, _: Thread, thread: Thread) -> None:
        if thread.guild.id != CONFIG.bot.guild_id:
            return

        await self.sync_channels(thread.guild)

    @Cog.listener()
    async def on_thread_channel_update(self, _: Thread, thread: Thread) -> None:
        if thread.guild.id != CONFIG.bot.guild_id:
            return

        await self.sync_channels(thread.guild)
