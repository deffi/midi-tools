#!/usr/bin/env python3

from typing import Optional
import socketserver

import rtmidi
import typer

from midi_tools import midi, SocketMidiBridge


class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, midi_in: Optional[rtmidi.MidiIn], midi_out: Optional[rtmidi.MidiOut], *args, **kwargs):
        self._midi_in = midi_in
        self._midi_out = midi_out
        super().__init__(*args, **kwargs)

    def handle(self):
        SocketMidiBridge(self.request, self._midi_in, self._midi_out, "-> ", "<- ").run()


def main(input_reference: str = typer.Option(None, "--in"),
         output_reference: str = typer.Option(None, "--out"),
         port: int = 6000):

    input_, input_name  = midi.open_input(input_reference)
    output, output_name = midi.open_output(output_reference)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    def create_request_handler(*args, **kwargs):
        return RequestHandler(input_, output, *args, **kwargs)

    with socketserver.TCPServer(("0.0.0.0", port), create_request_handler, bind_and_activate=False) as server:
        server.allow_reuse_address = True
        server.server_bind()
        server.server_activate()
        server.serve_forever()

if __name__ == "__main__":
    with midi.main():
        typer.run(main)
