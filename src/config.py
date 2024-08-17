from __future__ import annotations

import os
from pathlib import Path
from typing import Type

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr

from src.custom_argument_parser import CustomArgumentParser

load_dotenv()


class Config(BaseModel):
    _root: Path = Path(__file__).parent
    filenames: list[str] = Field(default_factory=list)
    huggingface_token: SecretStr = os.getenv("HUGGINGFACE_API_TOKEN") or ""
    huggingface_home: Path = Path("~/.cache/huggingface/hub")
    api_keys: list[str] = Field(default_factory=list)


def parse_arguments(config_class: Type[Config]):
    parser = CustomArgumentParser(
        description="Configure the application settings."
    )

    for name, value in config_class.model_fields.items():
        if name.startswith("_"):
            continue
        parser.add_argument(
            f"--{name}",
            type=value.annotation,
            default=value.default,
            help=f"Default: {value}",
        )

    return parser.parse_args()


def create_config_with_args(config_class: Type[Config], args) -> Config:
    config = config_class(
        **{name: getattr(args, name) for name in config_class.model_fields}
    )
    for variable in config.model_fields:
        value = getattr(config, variable)
        if (
            isinstance(value, Path)
            and value.suffix == ""
            and not value.exists()
        ):
            value.mkdir(parents=True)
    return config
