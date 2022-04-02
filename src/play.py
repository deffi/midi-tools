from time import sleep

from rtmidi.midiconstants import NOTE_ON, CONTROLLER_CHANGE, ALL_NOTES_OFF
import typer

from midi_tools import midi


def main(output_port: str = typer.Option(None, "--out")):
    output, output_name = midi.open_output(output_port)
    print(f"Output: {output_name}")

    output.send_message([NOTE_ON + 0, 60, 127])
    sleep(0.25)
    output.send_message([CONTROLLER_CHANGE + 0, ALL_NOTES_OFF, 0])
    sleep(0.5)


if __name__ == "__main__":
    with midi.main():
        typer.run(main)
