#!/usr/bin/env python3

import socket
import sys

from time import sleep
from typing import Optional
import socketserver

import rtmidi
import typer

from midi_tools import midi

class MidiHandler:
    sock = None

    def handle(self, event, data=None):
        if self.sock:
            message, _ = event
            self.sock.sendall(bytes(message))

def main(input_port: str = typer.Option(None, "--in"),
         output_port: str = typer.Option(None, "--out")):
    input_, input_name  = midi.open_input(input_port) if input_port else (None, None)
    output, output_name = midi.open_output(output_port) if output_port else (None, None)

    midi_handler = MidiHandler()
    input_.set_callback(midi_handler.handle)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect(("localhost", 6000))

        midi_handler.sock = sock

        while data := sock.recv(3):
            print(f"From ...: {data}")
            if output:
                output.send_message(list(data))
            print("recv...")

        print("after")



if __name__ == "__main__":
    with midi.main():
        typer.run(main)
