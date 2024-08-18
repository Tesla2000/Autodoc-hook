from __future__ import annotations

from pathlib import Path

from .config import Config
from .config import create_config_with_args
from .config import parse_arguments
from .transform.modify_file import modify_file


def main():
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    fails = 0
    paths = map(Path, config.filenames)
    for filepath in filter(lambda path: path.suffix == ".py", paths):
        fails |= modify_file(
            filepath,
            config=config,
        )
    return fails
