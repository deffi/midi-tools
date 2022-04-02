#!/usr/bin/env python3

from typing import Optional
import socketserver

import rtmidi
import typer

from midi_tools import midi, SocketMidiBridge


class RequestHandler(socketserver.BaseRequestHandler):
    input: Optional[rtmidi.MidiIn] = None
    output: Optional[rtmidi.MidiOut] = None

    def handle(self):
        SocketMidiBridge(self.request, self.input, self.output).run()


def main(input_reference: str = typer.Option(None, "--in"),
         output_reference: str = typer.Option(None, "--out"),
         port: int = 6000):

    input_, input_name  = midi.open_input(input_reference)
    output, output_name = midi.open_output(output_reference)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    RequestHandler.input = input_
    RequestHandler.output = output

    with socketserver.TCPServer(("0.0.0.0", port), RequestHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
