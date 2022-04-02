from socket import socket as sock
from typing import Optional

import rtmidi


class SocketMidiBridge:
    def __init__(self, socket: sock, midi_in: Optional[rtmidi.MidiIn], midi_out: Optional[rtmidi.MidiOut]):
        self._socket = socket
        self._midi_in = midi_in
        self._midi_out = midi_out

    def _handle_midi(self, event, _):
        message, _ = event
        self._socket.sendall(bytes(message))

    def run(self):
        if self._midi_in:
            self._midi_in.set_callback(self._handle_midi)

        try:
            while data := self._socket.recv(3):
                if self._midi_out:
                    self._midi_out.send_message(list(data))
        except ConnectionResetError:
            pass
        finally:
            if self._midi_in:
                self._midi_in.cancel_callback()
