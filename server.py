#!/usr/bin/env python3

from select import select
from socket import AF_INET, SOCK_STREAM, socket
from sys import argv, exit, stderr
from petition import Petition
from http_methods import handle_get, handle_delete, handle_post
from signal import signal, SIGINT


def setup() -> socket:
    """
    Create a socket for the server to listen
    """
    # Create a TCP/IP socket
    server = socket(AF_INET, SOCK_STREAM)
    server.setblocking(False)

    def sigint_handler(sig, frame):
        """
        Catches a SIGINT and cleans up
        """
        print("[i] Caught SIGINT, cleaning up...")
        server.close()
        exit(0)

    signal(SIGINT, sigint_handler)

    # Parse arguments
    if len(argv) != 2:
        print(f"Usage\n\t{argv[0]} <port>")
        exit(1)

    try:
        server_address = ('', int(argv[1]))
        print(f'starting up on port {server_address[1]}', file=stderr)
        server.bind(server_address)
    except ValueError as e:
        print(f"Error while trying to parse arguments {e}")
        exit(1)
    except OSError as e:
        print(f"Error while trying to bind to {argv[1]}: {e.strerror}")
        exit(1)

    # Listen for incoming connections
    server.listen(5)

    return server


def main():
    server = setup()

    # Sockets from which we expect to read
    inputs = [server]

    # This loop blocks until there is data ready
    while inputs:
        # Wait for at least one of the sockets to be ready for processing
        readable, writable, exceptional = select(inputs, [], [])

        # Handle inputs
        for s in readable:
            # A "readable" listening socket is ready to accept a connection
            if s is server:
                handle_new(s, inputs)

            # A message incoming from a client
            else:
                handle_msg(s, inputs, server)


def handle_new(s: socket, inputs: list[socket]):
    """
    Handles an incoming connection from a client
    """
    connection, client_address = s.accept()
    print('  connection from', client_address, file=stderr)
    connection.setblocking(False)
    inputs.append(connection)


def handle_msg(s: socket, inputs: list[socket], server: socket):
    """
    Handles a msg from an incomming connection, parses the request into a class
    and then forwards the request into the corresponding handler
    """
    buff = bytes()
    # Put the socket in a list to pass it to select with timeout
    s_list = [s]

    while True:
        readable, writable, exceptional = select(s_list, [], [], 10)

        data = s.recv(1024)

        if len(data) == 0:
            return

        buff += data
        slice_obj = slice(-1, -5, -1)

        last_chars = buff[slice_obj]

        if last_chars.decode() == "\n\r\n\r":
            break

    petition = Petition(data.decode())

    if len(petition.method) != 0:
        if petition.method == 'GET':
            handle_get(s, petition)

        elif petition.method == 'POST':
            handle_post(s, petition)

        elif petition.method == 'DELETE':
            handle_delete(s, petition)

    if not petition.keep_alive:
        addr, port = s.getpeername()
        print(f'  closing {addr}:{port}', file=stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        s.close()


if __name__ == "__main__":
    main()
