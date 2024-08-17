from __future__ import annotations

import os
import subprocess
import sys
import threading
from itertools import chain
from itertools import repeat
from pathlib import Path

from ...autodoc_hook.config import Config


def modify_file(filepath: Path, config: Config) -> int:
    """
    This function modifies a file by running a Docker container with a Python
    script that processes the file's content using a provided configuration. It
    utilizes Docker to execute the script, capturing both standard output and
    standard error, and then compares the output to the original file content.
    :param filepath: The `filepath` parameter represents the path to the file
    whose content will be modified.
    :param config: The `config` parameter is used to configure the script's
    behavior, including API keys and Hugging Face token.
    :return: The function returns an integer indicating the success or failure
    of the Docker build process.
    """
    code = filepath.read_text()

    docker_image = "fratajczak/autodoc"
    api_keys = list(
        chain.from_iterable(
            zip(
                repeat("-e"),
                (f"{key}={os.getenv(key)}" for key in config.api_keys),
            )
        )
    )
    python_script = [
        "python3",
        "main.py",
        "--code",
        code,
        "--huggingface_token",
        config.huggingface_token.get_secret_value(),
    ]
    command = (
        ["docker", "run", "--gpus", "all"]
        + api_keys
        + [
            "-v",
            f"{config.huggingface_home.expanduser().absolute()}:/code/models",
            "--rm",
            docker_image,
        ]
        + python_script
    )

    stdout_result = []
    stderr_result = []

    def read_output(pipe, result_list, print_function=None):
        """
        The `read_output` function reads lines from a given pipe, appending
        each line to a specified list and optionally printing it using a
        provided print function. After reading all lines, it closes the pipe to
        free up resources.
        :param pipe: A file-like object that provides a stream of data to be
        read line by line.
        :param print_function: A callable that processes each line read from
        the pipe, allowing for custom output handling.
        :param result_list: A list that stores each line read from the input
        pipe.
        :return: A list of lines read from the pipe.
        """
        for line in iter(pipe.readline, ""):
            result_list.append(line)
            if print_function:
                print_function(line)
        pipe.close()

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    try:
        stdout_thread = threading.Thread(
            target=read_output,
            args=(process.stdout, stdout_result, sys.stdout.write),
        )
        stderr_thread = threading.Thread(
            target=read_output,
            args=(process.stderr, stderr_result, sys.stderr.write),
        )

        stdout_thread.start()
        stderr_thread.start()

        stdout_thread.join()
        stderr_thread.join()

        return_code = process.wait()

    except KeyboardInterrupt:
        process.terminate()
        process.wait()
        print("\nProcess terminated by user.")
        return -1

    stdout_output = "".join(stdout_result)
    stderr_output = "".join(stderr_result)

    if return_code:
        print(stderr_output)
        print("Operation encountered errors.")

    if not return_code and code.strip() != stdout_output.strip():
        filepath.write_text(stdout_output)

    return return_code or code.strip() != stdout_output.strip()


if __name__ == "__main__":
    modify_file(Path(__file__), Config())
