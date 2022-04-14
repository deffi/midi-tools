from dataclasses import dataclass

from midi_tools.message import Message, Parser


@dataclass(frozen=True)
class FileTypeInfoRequestMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x06\x01"

    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x06,   0x01,   0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "FileTypeInfoRequestMessage":
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw)
