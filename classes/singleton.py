from __future__ import annotations

from typing import Any


class Singleton(type):
    """Singleton metaclass."""

    _instances: dict[type, object] = {}

    def __call__(cls, *args: list[Any] | None, **kwargs: list[Any] | None) -> object:
        """Singleton realization."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
