#!/usr/bin/env python3

from socket import socket as sock, AF_INET, SOCK_STREAM

import typer

from midi_tools import midi, SocketMidiBridge


def main(server: str,
         input_reference: str = typer.Option(None, "--in"),
         output_reference: str = typer.Option(None, "--out")):

    if ":" in server:
        host, port = server.split(":")
        port = int(port)
    else:
        host = server
        port = 6000

    input_, input_name  = midi.open_input(input_reference)
    output, output_name = midi.open_output(output_reference)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    with sock(AF_INET, SOCK_STREAM) as socket:
        socket.connect((host, port))
        SocketMidiBridge(socket, input_, output, "<- ", "-> ").run()


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
