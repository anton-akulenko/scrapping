

from __future__ import annotations

from typing import NamedTuple


class Arguments(NamedTuple):
    """Class with all arguments passed to script."""

    test_string_argument: str | None
    test_bool_argument: bool
