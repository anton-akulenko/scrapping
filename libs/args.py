# coding=utf-8
# Created by Ievgen Bryl at 25.03.2024

from __future__ import annotations

import argparse

from classes.arguments import Arguments


def process_arguments() -> Arguments:
    """Process all command line arguments and returns them as a class."""
    arg_parser = argparse.ArgumentParser(description="Project arguments help.")
    arg_parser.add_argument(
        "-test_string_argument",
        help="Test string argument",
        required=False,
        type=str,
        default=None,
        choices=[None, "one", "two", "three", "Bla-bla-bla!"],
    )
    arg_parser.add_argument("-test_bool_argument", action="store_true", help="Test boolean argument")

    arguments = arg_parser.parse_args()
    return Arguments(
        test_string_argument=arguments.test_string_argument,
        test_bool_argument=arguments.test_bool_argument,
    )
