import threading
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from pathlib import Path
from typing import Any
from typing import Dict

import ipywidgets as widgets
import jupytext
from IPython.display import display
from ipykernel.comm import Comm
from jsonrpcclient import request
from jsonrpcserver import dispatch
from jsonrpcserver import method
from watchdog.observers import Observer

from jupyter_ascending import server_multiplexer
from jupyter_ascending.json_requests import ExecuteRequest
from jupyter_ascending.json_requests import SyncRequest
from jupyter_ascending.logger import J_LOGGER
from jupyter_ascending.utils import find_free_port

_default_notebook = "/home/tj/git/untitled_ai/nb_extensions/jupyter_ascending/examples/introduction.status.py"
_EXECUTE_PORT_NUMBER = 12517
_EXECUTE_LOCATION = ("localhost", _EXECUTE_PORT_NUMBER)


@J_LOGGER.catch
def start_notebook_server_in_thread(notebook_name: str, file_watcher_enabled: bool = False, status_widget=None):
    """
    Args:
        notebook_name: The name of the notebook you want to be syncing in this process.
        file_watcher_enabled: If you're going to fire off events from a file watcher in your editor (like in PyCharm),
            then you don't need to enable this. It will just use the same HTTP requests as normal
    """

    notebook_path = Path(notebook_name).absolute()

    if not status_widget:
        status_widget = widgets.Text()
        status_widget.style.description_width = "300px"
        display(status_widget)

    if file_watcher_enabled:
        from jupyter_ascending.file_watcher import NotebookEventHandler

        event_handler = NotebookEventHandler(str(notebook_path.absolute()), file_watcher_enabled)
        file_observer = Observer()

        abs_path = str(notebook_path.parent.absolute())
        file_observer.schedule(event_handler, abs_path, recursive=False)
        file_watcher_thread = threading.Thread(target=file_observer.start, args=tuple())
        file_watcher_thread.start()

    # TODO: This might be a race condition if a bunch of these started at once...
    notebook_server_port = find_free_port()

    notebook_executor = HTTPServer(("localhost", notebook_server_port), NotebookKernelRequestHandler,)
    notebook_executor_thread = threading.Thread(target=notebook_executor.serve_forever, args=tuple())
    notebook_executor_thread.start()

    J_LOGGER.info("IPYTHON: Registering notebook {}", notebook_path)
    request(
        server_multiplexer.SERVER_URL,
        server_multiplexer.register_notebook_server.__name__,
        # Params
        notebook_path=str(notebook_path),
        port_number=notebook_server_port,
    )
    J_LOGGER.info("==> Success")

    return status_widget


@method
def handle_execute_request(data: dict) -> str:
    request = ExecuteRequest(**data)

    comm = make_comm("")
    execute_cell_contents(comm, request.cell_index)

    return f"Executing cell `{request.cell_index}`"


@method
def handle_sync_request(data: dict) -> str:
    request = SyncRequest(**data)

    comm = make_comm("")

    result = jupytext.reads(request.contents, fmt="py:percent")
    update_cell_contents(comm, result)

    return f"Syncing all cells"


class NotebookKernelRequestHandler(BaseHTTPRequestHandler):
    allow_reuse_address = True

    @J_LOGGER.catch
    def do_POST(self):
        J_LOGGER.info("=" * 80)
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()
        J_LOGGER.info("Notebook processing request:\n{}", request)

        response = dispatch(request)
        # Return response
        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())

        J_LOGGER.info("Got Response:\n{}", response)
        J_LOGGER.info("=" * 80)


def make_comm(notebook_src_path: str) -> Comm:
    comm_target_name = _make_comm_name(notebook_src_path)
    my_comm = Comm(target_name=comm_target_name)

    return my_comm


def update_cell_contents(comm: Comm, result: Dict[str, Any]) -> None:
    for index, written_cell in enumerate(result["cells"]):
        if written_cell["cell_type"] != "code":
            continue

        cell_contents = "".join(written_cell["source"])
        comm.send({"command": "update", "cell_number": index, "cell_contents": cell_contents})


def execute_cell_contents(comm: Comm, cell_number: int) -> None:
    comm.send({"command": "execute", "cell_number": cell_number})


def _make_comm_name(notebook_src_path: str) -> str:
    assert ".status." not in notebook_src_path

    return f"AUTO_SYNC::notebook"
