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
    print("Filenames:", config.filenames)
    for filename in map(Path, config.filenames):
        if filename.suffix != ".py":
            continue
        fails |= modify_file(
            filename,
            config=config,
        )
    return fails
