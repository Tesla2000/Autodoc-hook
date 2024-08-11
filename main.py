from __future__ import annotations

from pathlib import Path

from src.config import Config
from src.config import create_config_with_args
from src.config import parse_arguments
from src.transform.modify_file import modify_file


def main():
    args = parse_arguments(Config)
    config = create_config_with_args(Config, args)
    retv = 0
    for filename in map(Path, config.filenames):
        retv |= modify_file(
            filename,
            config=config,
        )
    return retv


if __name__ == "__main__":
    exit(main())
