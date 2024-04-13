from __future__ import annotations

import os

from dotenv import dotenv_values

from classes.singleton import Singleton


class Config(metaclass=Singleton):
    """Class for store all project settings."""

    SETTING_EXAMPLE: str

    def __init__(self) -> None:
        """Load settings from file."""
        tmp = dotenv_values(dotenv_path=os.path.join(".env", ".env"))

        assert tmp["SETTING_EXAMPLE"] is not None
        self.SETTING_EXAMPLE = tmp["SETTING_EXAMPLE"]


CONFIG = Config()
