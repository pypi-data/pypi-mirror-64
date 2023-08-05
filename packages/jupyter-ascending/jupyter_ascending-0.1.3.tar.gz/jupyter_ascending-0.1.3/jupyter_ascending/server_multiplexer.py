import threading
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

import attr
from jsonrpcclient import request
from jsonrpcserver import dispatch
from jsonrpcserver import methods

from jupyter_ascending.json_requests import ExecuteRequest
from jupyter_ascending.json_requests import JsonBaseRequest
from jupyter_ascending.json_requests import SyncRequest
from jupyter_ascending.logger import J_LOGGER
from jupyter_ascending.syncer import handle_execute_request
from jupyter_ascending.syncer import handle_sync_request

SERVER_PORT_NUMBER = 12517
SERVER_HOST_LOCATION = ("localhost", SERVER_PORT_NUMBER)
SERVER_URL = f"http://{SERVER_HOST_LOCATION[0]}:{SERVER_HOST_LOCATION[1]}"

GenericJsonRequest = TypeVar("GenericJsonRequest", bound=JsonBaseRequest)

_REGISTERED_SERVERS: Dict[str, int] = {}


multiplexer_methods = methods.Methods()


@multiplexer_methods.add
def register_notebook_server(notebook_path: str, port_number: int) -> None:
    register_server(notebook_path=notebook_path, port_number=port_number)


@multiplexer_methods.add
def perform_notebook_request(notebook_path: str, command_name: str, data: Dict[str, Any]) -> None:
    J_LOGGER.debug("Perforing notebook request... ")

    notebook_server = get_server_for_notebook(notebook_path)
    if notebook_server is None:
        J_LOGGER.info("==> Unable to process request")
        return

    request(notebook_server, command_name, data=data)


class ServerMultiplexer(BaseHTTPRequestHandler):
    """
    Class that runs in the jupyter notebook server.
        Note that is not the same thing as the jupyter kernel that you'll be running.
        This is a persistent connection that runs in the main server.

    It will handle multiplexing the requests to the correct notebook kernels, which will allow
        multiple notebooks to be synced simultaneously.
    """

    allow_reuse_address = True

    def do_POST(self):
        # Process request
        request = self.rfile.read(int(self.headers["Content-Length"])).decode()

        J_LOGGER.info("=" * 80)
        J_LOGGER.info("Processing request:\n{}", request)
        response = dispatch(request, methods=multiplexer_methods)
        J_LOGGER.info("Got Response:\n{}", response)
        J_LOGGER.info("=" * 80)

        self.send_response(response.http_status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(str(response).encode())


def register_server(notebook_path: str, port_number: int) -> None:
    J_LOGGER.info("Registering notebook {notebook} on port {port}", notebook=notebook_path, port=port_number)

    _REGISTERED_SERVERS[notebook_path] = port_number

    J_LOGGER.debug("Updated notebook mappings: {}", _REGISTERED_SERVERS)


def get_server_for_notebook(notebook_path: str) -> Optional[str]:
    # Normalize to notebook path
    notebook_path = notebook_path.replace(".synced.py", ".synced.ipynb")

    J_LOGGER.debug("Finding server for notebook_path, script_path: {}", notebook_path)

    potential_notebooks: List[str] = []
    for registered_name in _REGISTERED_SERVERS:
        if registered_name in notebook_path:
            potential_notebooks.append(registered_name)

    if len(potential_notebooks) > 1:
        J_LOGGER.warning("Found more than one notebook {}, {}", notebook_path, potential_notebooks)
        return None
    elif len(potential_notebooks) == 1:
        notebook_port = _REGISTERED_SERVERS[potential_notebooks[0]]

        J_LOGGER.debug("Found server at port {}", notebook_port)
        return f"http://localhost:{notebook_port}"
    else:
        J_LOGGER.warning("Could not find server for notebook_path: {}", notebook_path)
        return None


def request_notebook_command(json_request: GenericJsonRequest):
    request(
        SERVER_URL,
        perform_notebook_request.__name__,
        command_name=_map_json_request_to_function_name(json_request),
        notebook_path=json_request.file_name,
        data=attr.asdict(json_request),
    )


def _map_json_request_to_function_name(json_request: GenericJsonRequest) -> str:
    if isinstance(json_request, ExecuteRequest):
        return handle_execute_request.__name__
    elif isinstance(json_request, SyncRequest):
        return handle_sync_request.__name__
    else:
        assert False, json_request


def start_server_in_thread():
    J_LOGGER.info("Starting Server...")

    server_executor = HTTPServer(SERVER_HOST_LOCATION, ServerMultiplexer)
    server_executor_thread = threading.Thread(target=server_executor.serve_forever, args=tuple())
    server_executor_thread.start()

    J_LOGGER.info("... Started Server")

    return server_executor
