#!/usr/bin/env python3

from socket import socket as sock, AF_INET, SOCK_STREAM

import typer

from midi_tools import midi, SocketMidiBridge


def main(input_port: str = typer.Option(None, "--in"),
         output_port: str = typer.Option(None, "--out")):
    input_, input_name  = midi.open_input(input_port)
    output, output_name = midi.open_output(output_port)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    with sock(AF_INET, SOCK_STREAM) as socket:
        socket.connect(("localhost", 6000))
        SocketMidiBridge(socket, input_, output).run()


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
