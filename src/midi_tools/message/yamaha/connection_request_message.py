
from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class ConnectionRequestMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x01\x01"

    def __post_init__(self):
        pass

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x01,   0x01,   0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "ConnectionRequestMessage":
        assert raw == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x01,   0x01,   0xF7])

        return cls(raw)
