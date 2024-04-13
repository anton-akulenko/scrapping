# coding=utf-8
# Created by Ievgen Bryl at 23.03.2024

from __future__ import annotations

from random import SystemRandom
import string


def generate_rnd_string(length: int = 64) -> str:
    """Generate random string AZ09 with requested length."""
    return "".join(SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
