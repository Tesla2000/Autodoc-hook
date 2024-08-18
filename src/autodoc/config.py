from __future__ import annotations

import os
from argparse import Namespace
from pathlib import Path
from typing import Type

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import Field
from pydantic import SecretStr

from .custom_argument_parser import CustomArgumentParser

load_dotenv()


class Config(BaseModel):
    _root: Path = Path(__file__).parent
    filenames: list[str] = Field(default_factory=list)
    huggingface_token: SecretStr = os.getenv("HUGGINGFACE_API_TOKEN") or ""
    huggingface_home: Path = Path("~/.cache/huggingface/hub")
    api_keys: list[str] = Field(default_factory=list)
    llm: str = "gpt-4o-mini"


def parse_arguments(config_class: Type[Config]) -> Namespace:
    """
    This function parses command-line arguments based on a configuration class.
    It creates an argument parser, adds arguments for each field in the
    configuration class, and handles default values and help messages.
    :param config_class: `config_class` is a type that defines the fields and
    their corresponding types for configuring the application settings.
    :return: A `ArgumentParser` object for parsing command-line arguments.
    """
    parser = CustomArgumentParser(
        description="Configure the application settings."
    )

    for name, value in config_class.model_fields.items():
        if name.startswith("_"):
            continue
        parser.add_argument(
            name if name == "filenames" else f"--{name}",
            type=value.annotation,
            default=value.default,
            help=f"Default: {value}",
        )

    return parser.parse_args()


def create_config_with_args(config_class: Type[Config], args) -> Config:
    """
    This function creates a configuration object of a specified class
    (`config_class`) using arguments provided (`args`). It then ensures that
    any paths within the configuration object's fields exist by creating them
    if they don't.
    :param config_class: `config_class` is a type of configuration class that
    defines the structure of the configuration object.
    :param args: `args` is a dictionary containing the arguments to be used to
    initialize the configuration object.
    :return: A configured object with model fields populated and directories
    created as needed.
    """
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
