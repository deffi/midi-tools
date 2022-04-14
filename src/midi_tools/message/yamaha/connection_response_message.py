from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class ConnectionResponseMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x01\x02"

    payload: bytes

    def __post_init__(self):
        assert len(self.payload) == 1

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x01,   0x02]) + self.payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "ConnectionResponseMessage":
        assert len(raw) == 9
        assert raw[0:7] == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x01,   0x02])
        payload = raw[7:8]
        assert raw[8] == bytes([0xF7])

        return cls(raw, payload)
