from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class InstrumentDataResponseMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x02\x02"

    payload: bytes

    def __post_init__(self):
        assert len(self.payload) <= 127

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x02,   0x02, len(self.payload)]) + self.payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "InstrumentDataResponseMessage":
        # f0 43 50   0 0 2   len data
        assert len(raw) >= 7
        assert raw[0:7] == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x02,   0x02])
        length = raw[7]
        assert len(raw) == 7 + length + 1
        payload = raw[7:7+length]
        assert raw[7+length] == bytes([0xF7])

        return cls(raw, payload)
