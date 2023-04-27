from asyncio import Event
from datetime import datetime
from typing import Any, Optional

from disnake.ext.commands import Bot as _Bot
from disnake.ext.commands import Context as _Context
from loguru import logger

from src.core.database import database


class Context(_Context[_Bot]):
    pass


class Bot(_Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.online_since: Optional[datetime] = None
        self.sync_completed = Event()

    async def start(self, *args: Any, reconnect: bool = True, **kwargs: Any) -> None:
        logger.info("Connecting to database...")
        await database.connect()
        logger.info("Connected to database.")

        self.online_since = datetime.utcnow()

        await super().start(*args, reconnect=reconnect, **kwargs)

    async def on_connect(self) -> None:
        logger.info(f"Bot connected to the gateway, logged in as {str(self.user)}.")

    async def on_ready(self) -> None:
        logger.info("READY event received.")

    def load_extension(self, name: str, *, package: Optional[str] = None) -> None:
        super().load_extension(name, package=package)

        logger.info(f"Loaded extension {name}.")
