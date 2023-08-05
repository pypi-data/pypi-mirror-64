import argparse
from pathlib import Path

import jupytext

from jupyter_ascending import server_multiplexer
from jupyter_ascending.json_requests import SyncRequest


def send(file_name: str, fmt: str = "py:percent", force_update: bool = False):
    if ".synced.py" not in file_name:
        return

    file_name = str(Path(file_name).absolute())

    notebook_name = file_name.replace(".synced.py", ".synced.ipynb")
    notebook_path = Path(notebook_name)

    with open(file_name, "r") as reader:
        raw_result = reader.read()

    if not notebook_path.exists() or force_update:
        # TODO: Could just only update cells?
        notebook_contents = jupytext.reads(raw_result, fmt=fmt)
        with open(notebook_path, "w") as writer:
            writer.write(notebook_contents + "\n")

    request_obj = SyncRequest(file_name=file_name, contents=raw_result)
    server_multiplexer.request_notebook_command(request_obj)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--filename", help="Filename to send")

    arguments = parser.parse_args()
    send(arguments.filename)
