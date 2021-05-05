from petition import Petition
from datetime import date
from socket import socket
from typing import Dict, Callable
from datetime import datetime
import mimetypes


router: Dict[str, Callable[[socket, Petition], None]] = {}


def handle_log_query(s: socket, p: Petition):
    """
    Simply logs the request and returns OK
    """
    data = "OK".encode()

    print(f"[i] Got {p.header_map}")

    resp = craft_response("200 OK", "text/plain", data)
    s.sendall(resp)


def handle_time_query(s: socket, p: Petition):
    """
    Returns the current date and time in the utc timezone
    """
    data = str(datetime.utcnow()).encode()

    resp = craft_response("200 OK", "text/plain", data)
    s.sendall(resp)


def register_functions():
    """
    Registers the log and time endpoints
    """
    router["/api/time"] = handle_time_query
    router["/api/log"] = handle_log_query


def handle_post(s: socket, petition: Petition):
    pass


def handle_delete(s: socket, petition: Petition):
    pass


def handle_get(s: socket, petition: Petition):
    """
    Handles a get petition
    """
    path = petition.arguments[0]

    try:
        route_handler = router[path]
        route_handler(s, petition)
        return
    except KeyError:
        pass

    if path[-1] == '/':
        path += "index.html"

    mime, _ = mimetypes.guess_type(path)

    if mime is None:
        mime = "text/plain"

    print(f"[i] GET for \"{path}\" with {petition.header_map}")

    try:
        with open("./" + path, "rb") as file:
            data = file.read()
            resp = craft_response("200 OK", mime, data)
    except FileNotFoundError:
        resp = craft_response("404 NOT FOUND", mime, ''.encode())

    s.setblocking(True)
    s.sendall(resp)
    s.setblocking(False)


def craft_response(status: str, mime: str, data: bytes) -> bytes:
    header_status = f"HTTP/1.1 {status}\r\n"
    header_date = f"Date: {str(date.today())}\r\n"
    header_server = "Server: Anarres\r\n"
    header_mime = f"Content-type: {mime}\r\n"
    header_length = f"Content-length: {len(data)}\r\n"
    header_connection = f"Connection: {'close'}\r\n\r\n"

    response = header_status + header_date + header_server + header_mime + header_length + header_connection

    rsp = response.encode() + data

    return rsp
