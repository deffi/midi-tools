from socket import socket as sock
from typing import Optional, List

import rtmidi


class SocketMidiBridge:
    def __init__(self, socket: sock,
                 midi_in: Optional[rtmidi.MidiIn], midi_out: Optional[rtmidi.MidiOut],
                 socket_prefix: Optional[str] = None, midi_prefix: Optional[str] = None,
                 ascii: bool = False):
        self._socket = socket
        self._midi_in = midi_in
        self._midi_out = midi_out
        self._socket_prefix = socket_prefix
        self._midi_prefix = midi_prefix
        self._ascii = ascii

    def _format_message(self, message: List[int], prefix: str) -> str:
        hex = " ".join(f"{m:02X}" for m in message)

        def render(value: int) -> str:
            if 32 <= value < 127:
                return chr(value)
            else:
                return " "

        if self._ascii:
            ascii = " ".join(render(m) + " " for m in message)
            return prefix + hex + "\n" + "|" + " " * (len(prefix)-1) + ascii
        else:
            return prefix + hex

    def _handle_midi(self, event, _):
        message, _ = event
        self._socket.sendall(len(message).to_bytes(4, "big") + bytes(message))
        if self._midi_prefix is not None:
            print(self._format_message(message, self._midi_prefix))

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

        try:
            while True:
                length = self._receive_length()
                if length is None:
                    break

                data = self._receive_data(length)
                if data is None:
                    break

                if self._midi_out:
                    message = list(data)
                    self._midi_out.send_message(message)
                    if self._socket_prefix is not None:
                        print(self._format_message(message, self._socket_prefix))

        except ConnectionResetError:
            pass
        finally:
            if self._midi_in:
                self._midi_in.cancel_callback()
