#!/usr/bin/env python3

from select import select
from socket import AF_INET, SOCK_STREAM, socket
from sys import argv, exit, stderr


def setup() -> socket:
    """
    Create a socket for the server to listen
    """
    # Create a TCP/IP socket
    server = socket(AF_INET, SOCK_STREAM)
    server.setblocking(False)

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
    buff = ""

    while True:
        data = s.recv(1024)

        if len(data) == 0:
            return

        buff += data
        slice_obj = slice(-1, -5, -1)

        if buff[slice_obj] == "\n\r\n\r"
            break

    petition = Petition(data)

    if petition.data:
        if petition.method == 'GET':
            handle_get(petition)

        elif petition.method == 'POST':
            handle_post(petition)

        elif petition.method == 'DELETE':
            handle_delete(petition)

    if not petition.keep_alive:
        # Interpret empty result as closed connection
        print(f'  closing {addr}:{port}', file=stderr)
        # Stop listening for input on the connection
        inputs.remove(s)
        s.close()


if __name__ == "__main__":
    main()

