from contextlib import contextmanager
from typing import Sequence, Optional, Any, TypeVar, Type

import rtmidi

from midi_tools.util.int import is_int


MidiInOut = TypeVar("MidiInOut", rtmidi.MidiIn, rtmidi.MidiOut)


class AmbiguousPort(RuntimeError):
    pass


def resolve_name(names: Sequence[str], reference: Optional[str]) -> Optional[int]:
    if reference is None:
        return None

    elif is_int(reference):
        return int(reference)

    else:
        candidates = [index for index, name in enumerate(names) if reference.lower() in name.lower()]
        if len(candidates) == 1:
            return candidates[0]
        else:
            raise AmbiguousPort(reference)


def open_port(port_type: Type[MidiInOut], reference: Optional[str]) -> (Optional[MidiInOut], Optional[str]):
    # Create a port of the specified type
    port = port_type()

    # Determine the index of the specified port
    port_names = port.get_ports()
    index = resolve_name(port_names, reference)

    # Open the port and return it along with its name. Exception: if index is
    # None, return (None, None).
    if index is None:
        return None, None
    else:
        port.open_port(index)
        return port, port_names[index]


def open_input(reference: Optional[str]) -> (rtmidi.MidiIn, str):
    return open_port(rtmidi.MidiIn, reference)


def open_output(reference: Optional[str]) -> (rtmidi.MidiOut, str):
    return open_port(rtmidi.MidiOut, reference)


@contextmanager
def main():
    try:
        yield
    except AmbiguousPort as e:
        print(f"Ambiguous port specified: {e}")
        print(f"Available input ports:")
        for index, port_name in enumerate(rtmidi.MidiIn().get_ports()):
            print(f"    {index}: {port_name}")
        print(f"Available output ports:")
        for index, port_name in enumerate(rtmidi.MidiOut().get_ports()):
            print(f"    {index}: {port_name}")
