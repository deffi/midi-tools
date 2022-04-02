from time import sleep
from typing import Optional

import rtmidi
import typer

from midi_tools import midi


class MidiBridge:
    def __init__(self, input_: rtmidi.MidiIn, output: rtmidi.MidiOut, prefix: str):
        self.input = input_
        self.output = output
        self.prefix = prefix

    def start(self):
        self.input.ignore_types(sysex=False, timing=False, active_sense=True)
        self.input.set_callback(self._received)

    def _received(self, event, data=None):
        message, delta_time = event
        message_text = " ".join(f"{m:02X}" for m in message)
        self.output.send_message(message)
        print(f"{delta_time:0.2f} {self.prefix}{message_text}")


def start_bridge(input_name: Optional[str], output_name: Optional[str], prefix: Optional[str] = None):
    input_, input_name  = midi.open_input(input_name)
    output, output_name = midi.open_output(output_name)

    if prefix is None:
        prefix = f"{input_name} -> {output_name}: "
        print(prefix)
    else:
        print(f"{prefix}: {input_name} -> {output_name}")

    MidiBridge(input_, output, prefix).start()


def main(input_port: str = typer.Option(None, "--in"),
         output_port: str = typer.Option(None, "--out")):

    start_bridge(input_port, output_port)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
