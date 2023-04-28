from pathlib import Path
from typing import Any, List, Optional

from pydantic import BaseModel
from yaml import safe_load


class PythonConfig(BaseModel):
    log_level: str = "INFO"


class BotConfig(BaseModel):
    prefix: str = "!"
    guild_id: int
    ignored_categories: List[int] = []
    ignored_channels: List[int] = []
    staff_categories: List[int] = []
    staff_channels: List[int] = []


class Config(BaseModel):
    python: PythonConfig = PythonConfig()
    bot: BotConfig


_raw_data = Path(f"./config.yml").read_text()
_data: dict[str, Any] = safe_load(_raw_data) or {}

CONFIG = Config(**_data)
