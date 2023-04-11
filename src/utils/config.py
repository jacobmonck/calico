from os import getenv
from pathlib import Path
from typing import Any, List, Optional

from pydantic import BaseModel
from yaml import safe_load


class PythonConfig(BaseModel):
    log_level: Optional[str] = "INFO"


class BotConfig(BaseModel):
    prefix: str = "!"
    guild_id: str
    staff_categories: Optional[List[int]]
    staff_channels: Optional[List[str]]


class Config(BaseModel):
    python: Optional[PythonConfig] = None
    bot: BotConfig


_raw_data = Path(f"./config.yml").read_text()
_data: dict[str, Any] = safe_load(_raw_data) or {}

CONFIG = Config(**_data)
