from __future__ import annotations

from pathlib import Path

from src.config import Config
from src.config import create_config_with_args
from src.config import parse_arguments
from src.transform.modify_file import modify_file


def main():
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    fails = 0
    for filename in map(Path, config.filenames):
        if filename.suffix != ".py":
            continue
        fails |= modify_file(
            filename,
            config=config,
        )
    return fails


if __name__ == "__main__":
    exit(main())
