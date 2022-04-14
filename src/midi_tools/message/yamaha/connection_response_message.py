from dataclasses import dataclass

from midi_tools.message import Message, Parser


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
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        payload = parser.get_data(2)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw, payload)
