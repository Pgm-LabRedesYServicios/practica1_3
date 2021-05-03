from petition import Petition
from datetime import date
from socket import socket
import mimetypes


router = {}


def handle_delete(petition: Petition):
    pass


def handle_get(s: socket, petition: Petition):
    """
    Handles a get petition
    """
    path = petition.arguments[0]

    try:
        function = router[path]
        function(petition)
        return
    except KeyError:
        pass

    if path[-1] == '/':
        path += "index.html"

    mime, _ = mimetypes.guess_type(path)

    try:
        with open("./" + path) as file:
            data = file.read()
            resp = craft_response("200 OK", mime, data)
            print(resp.decode())
    except FileNotFoundError:
        resp = craft_response("404 NOT FOUND", mime, '')

    s.sendall(resp)


def craft_response(status, mime, data):
    header_status = f"HTTP/1.1 {status}\r\n"
    header_date = f"Date: {str(date.today())}\r\n"
    header_server = "Server: Anarres\r\n"
    header_mime = f"Content-type: {mime}\r\n"
    header_length = f"Content-length: {len(data)}\r\n"
    header_connection = f"Connection: {'close'}\r\n\r\n{data}"

    response = header_status + header_date + header_server + header_mime + header_length + header_connection

    return response.encode()
