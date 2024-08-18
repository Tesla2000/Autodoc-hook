from __future__ import annotations

from pathlib import Path

from .config import Config
from .config import create_config_with_args
from .config import parse_arguments
from .transform.modify_file import modify_file


def main():
    """
    This function processes a list of Python files based on configuration
    parameters, modifying each file and returning a flag indicating any
    failures encountered. It iterates through the files, applying modifications
    defined by the configuration and reporting any errors encountered.
    :return: Number of files modified that failed.
    """
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    fail = 0
    paths = map(Path, config.filenames)
    for filepath in filter(lambda path: path.suffix == ".py", paths):
        fail |= modify_file(
            filepath,
            config=config,
        )
    return fail
