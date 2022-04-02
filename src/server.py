#!/usr/bin/env python3

from time import sleep
from typing import Optional
import socketserver

import rtmidi
import typer

from midi_tools import midi


class RequestHandler(socketserver.BaseRequestHandler):
    input: Optional[rtmidi.MidiIn] = None
    output: Optional[rtmidi.MidiOut] = None

    def handle_midi(self, event, data=None):
        message, _ = event
        self.request.sendall(bytes(message))

    def setup(self):
        if self.input:
            self.input.set_callback(self.handle_midi)

    def handle(self):
        print("Handler")

        while data := self.request.recv(3):
            print(f"From {self.client_address}: {data}")
            if self.output:
                self.output.send_message(list(data))

        print("Bye")

    def finish(self) -> None:
        if self.input:
            self.input.cancel_callback()


def main(input_port: str = typer.Option(None, "--in"),
         output_port: str = typer.Option(None, "--out")):
    input_, input_name  = midi.open_input(input_port) if input_port else (None, None)
    output, output_name = midi.open_output(output_port) if output_port else (None, None)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    RequestHandler.input = input_
    RequestHandler.output = output

    with socketserver.TCPServer(("0.0.0.0", 6000), RequestHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
