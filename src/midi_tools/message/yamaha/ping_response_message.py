from dataclasses import dataclass

from midi_tools.message import Message, Parser


@dataclass(frozen=True)
class PingResponseMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x00\x02"

    payload: bytes

    def __post_init__(self):
        assert self.payload == bytes([0x01, 0x01])

    def to_message(self) -> bytes:
        return self.prefix + self.payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "PingResponseMessage":
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        payload = parser.get_data(2)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw, payload)
