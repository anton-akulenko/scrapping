from __future__ import annotations

import datetime


class PropertyWrapper:
    """Temporary class for use function as a property."""

    @property
    def datetime_now(self) -> datetime.datetime:
        """Return now as a property."""
        return datetime.datetime.now()
