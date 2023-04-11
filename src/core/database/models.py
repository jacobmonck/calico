from datetime import datetime
from typing import Optional

from ormar import JSON, BigInteger, Boolean, DateTime, ForeignKey, Integer, Model, Text

from src.core.database import ParentMeta


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
    created_at: datetime = DateTime()
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
    avatar_hash: str = Text(nullable=True)
    guild_avatar_hash: str = Text(nullable=True)
    created_at: datetime = DateTime()
    joined_at: datetime = DateTime()
    in_guild: bool = Boolean(default=True)
    pending: bool = Boolean()
    staff: bool = Boolean()
    flags: dict = JSON()


class Message(Model):
    class Meta(ParentMeta):
        tablename = "messages"

    id: int = BigInteger(primary_key=True)
    created_at: datetime = DateTime()
    deleted: bool = Boolean()
    author: Optional[User] = ForeignKey(User)
    channel: Optional[Channel] = ForeignKey(Channel)
    thread: Optional[Thread] = ForeignKey(Thread)
