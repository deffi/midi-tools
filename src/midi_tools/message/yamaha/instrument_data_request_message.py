from dataclasses import dataclass

from midi_tools.message import Message, Parser


@dataclass(frozen=True)
class InstrumentDataRequestMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x02\x01"

    def to_message(self) -> bytes:
        return self.prefix + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "InstrumentDataRequestMessage":
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw)
