from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class PingResponseMessage(Message):
    payload: bytes

    def __post_init__(self):
        assert self.payload == bytes([0x01, 0x01])

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x00,   0x02]) + self.payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "PingResponseMessage":
        assert len(raw) == 10
        assert raw[0:7] == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x00,   0x02])
        payload = raw[7:9]
        assert raw[9] == bytes([0xF7])

        return cls(raw, payload)
