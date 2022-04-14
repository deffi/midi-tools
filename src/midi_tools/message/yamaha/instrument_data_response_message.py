from dataclasses import dataclass

from midi_tools.message import Message, Parser


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
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        length = parser.get_integer(1)
        payload = parser.get_data(length)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw, payload)
