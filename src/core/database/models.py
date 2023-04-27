from datetime import datetime
from os import environ
from typing import Any, List, Optional

from asyncpg import create_pool
from loguru import logger
from more_itertools import chunked
from ormar import (
    JSON,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Model,
    SmallInteger,
    Text,
)

from src.core.database import ParentMeta, database
from src.core.database.db import TZDateTime


class Category(Model):
    class Meta(ParentMeta):
        tablename = "categories"

    id: int = BigInteger(primary_key=True)
    name: str = Text()


class Channel(Model):
    class Meta(ParentMeta):
        tablename = "channels"

    id: int = BigInteger(primary_key=True)
    name: str = Text()
    staff: bool = Boolean()
    category: Optional[Category] = ForeignKey(Category)


class Thread(Model):
    class Meta(ParentMeta):
        tablename = "threads"

    id: int = BigInteger(primary_key=True)
    name: str = Text()
    created_at: datetime = DateTime(nullable=True)
    archived: bool = Boolean(default=False)
    auto_archive_duration: int = Integer()
    locked: bool = Boolean(default=False)
    type: str = Text()


class User(Model):
    class Meta(ParentMeta):
        tablename = "users"

    id: int = BigInteger(primary_key=True)
    username: str = Text()
    nickname: str = Text(nullable=True)
    discriminator: int = SmallInteger()
    avatar_hash: str = Text(nullable=True)
    guild_avatar_hash: str = Text(nullable=True)
    created_at: datetime = DateTime()
    joined_at: datetime = DateTime()
    in_guild: bool = Boolean(default=True)
    pending: bool = Boolean()
    flags: dict = JSON()

    @classmethod
    async def bulk_upsert(cls, users: List[List[Any]]) -> None:
        chunks = chunked(users, 1500)

        # We create a connection pool here because Ormar had extremly poor performance
        # when using the execute_many() method so this is a more performant solution.
        pool = await create_pool(environ["DB_URI"])
        if not pool:
            logger.error("Failed to establish a connection pool with the database.")
            exit()

        for chunk in chunks:
            async with pool.acquire() as conn:
                await conn.executemany(
                    """
                    INSERT INTO users 
                    (
                        id, 
                        username,
                        nickname, 
                        discriminator,
                        avatar_hash,
                        guild_avatar_hash,
                        created_at,
                        joined_at,
                        in_guild,
                        pending,
                        flags
                    )
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                    ON CONFLICT (id)
                    DO UPDATE SET
                        username = EXCLUDED.username,
                        nickname = EXCLUDED.nickname,
                        discriminator = EXCLUDED.discriminator,
                        avatar_hash = EXCLUDED.avatar_hash,
                        guild_avatar_hash = EXCLUDED.guild_avatar_hash,
                        created_at = EXCLUDED.created_at,
                        joined_at = EXCLUDED.joined_at,
                        in_guild = EXCLUDED.in_guild,
                        pending = EXCLUDED.pending,
                        flags = EXCLUDED.flags;
                    """,
                    chunk,
                )
                logger.trace(f"Bulk upsert performed, {len(chunk)} rows affected.")

        await pool.close()


class Message(Model):
    class Meta(ParentMeta):
        tablename = "messages"

    id: int = BigInteger(primary_key=True)
    created_at: datetime = DateTime()
    deleted: bool = Boolean()
    author: Optional[User] = ForeignKey(User)
    channel: Optional[Channel] = ForeignKey(Channel)
    thread: Optional[Thread] = ForeignKey(Thread)
