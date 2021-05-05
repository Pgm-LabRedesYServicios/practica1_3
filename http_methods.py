from petition import Petition
from datetime import date
from socket import socket
from typing import Dict, Callable
import mimetypes


router: Dict[str, Callable[[socket, Petition], None]] = {}


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

    s.sendall(resp)


def craft_response(status: str, mime: str, data: bytes):
    header_status = f"HTTP/1.1 {status}\r\n"
    header_date = f"Date: {str(date.today())}\r\n"
    header_server = "Server: Anarres\r\n"
    header_mime = f"Content-type: {mime}\r\n"
    header_length = f"Content-length: {len(data)}\r\n"
    header_connection = f"Connection: {'close'}\r\n\r\n"

    response = header_status + header_date + header_server + header_mime + header_length + header_connection

    rsp = response.encode() + data

    return rsp
