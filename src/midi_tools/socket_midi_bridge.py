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
        self._socket.sendall(len(message).to_bytes(4, "big") + bytes(message))

    def _receive_length(self) -> Optional[int]:
        data = self._socket.recv(4)

        if not data:
            return None

        assert len(data) == 4
        return int.from_bytes(data, "big")

    def _receive_data(self, length) -> Optional[bytes]:
        buffer = bytes()

        while True:
            data = self._socket.recv(length - len(buffer))
            if not data:
                return None

            buffer += data
            if len(buffer) == length:
                return buffer

    def run(self):
        if self._midi_in:
            self._midi_in.set_callback(self._handle_midi)

        buffer = bytes()

        try:
            while True:
                length = self._receive_length()
                if length is None:
                    break

                data = self._receive_data(length)
                if data is None:
                    break

                if self._midi_out:
                    self._midi_out.send_message(list(data))
        except ConnectionResetError:
            pass
        finally:
            if self._midi_in:
                self._midi_in.cancel_callback()
