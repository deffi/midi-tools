#!/usr/bin/env python3

from time import sleep
from typing import Optional

import rtmidi
import typer

from midi_tools import midi
from midi_tools.util import hex
from midi_tools.message import Message
from midi_tools.message.factory import create_message
from midi_tools.message import yamaha


class FakePiano:
    def __init__(self, input_: rtmidi.MidiIn, output: rtmidi.MidiOut):
        self.input = input_
        self.output = output

    def start(self):
        self.input.ignore_types(sysex=False, timing=False, active_sense=True)
        self.input.set_callback(self._received)
        print("Starting fake piano")

    def send_message(self, message: Message):
        raw_message = message.to_message()
        print(f"<- {message} ({hex.render(raw_message)})")
        self.output.send_message(raw_message)

    def _received(self, event, data=None):
        raw_message, delta_time = event
        raw_message = bytes(raw_message)

        message = create_message(raw_message)
        if message:
            print(f"-> {message} ({hex.render(raw_message)})")
        else:
            print(f"-> {hex.render(raw_message)}")

        if isinstance(message, yamaha.PingRequestMessage):
            self.send_message(yamaha.PingResponseMessage(None, b"\x01\x01"))
        elif isinstance(message, yamaha.InstrumentDataRequestMessage):
            self.send_message(yamaha.InstrumentDataResponseMessage(None, hex.parse("00 01 00 00 01 00 01 00 00 39 18 01 14 01 00 00 00 00 00 00 01 7F 00 00 00 32 00 00 00 00 00 00 00 00 00 00 00 00 00 00 27 08 00 00 02 00 03 19 00 00")))
        elif isinstance(message, yamaha.FileTypeInfoRequestMessage):
            self.send_message(yamaha.FileTypeInfoResponseMessage(None, b".MID;.PLS;.LOG"))
        elif isinstance(message, yamaha.ConnectionRequestMessage):
            print("Connect")
            self.send_message(yamaha.ConnectionResponseMessage(None, b"\x00"))
        elif isinstance(message, yamaha.DisconnectRequestMessage):
            print("Disconnect")


def main(input_port: str = typer.Option(None, "--in"),
         output_port: str = typer.Option(None, "--out")):

    input_, input_name  = midi.open_input(input_port)
    output, output_name = midi.open_output(output_port)

    print(f"Input:  {input_name}")
    print(f"Output: {output_name}")

    FakePiano(input_, output).start()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
