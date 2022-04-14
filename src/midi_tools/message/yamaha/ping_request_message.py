
from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class PingRequestMessage(Message):
    def __post_init__(self):
        pass

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x00,   0x01,   0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "PingRequestMessage":
        assert raw == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x00,   0x01,   0xF7])

        return cls(raw)
