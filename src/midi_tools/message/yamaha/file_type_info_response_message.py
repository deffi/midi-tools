from dataclasses import dataclass

from midi_tools.util.message import encode
from midi_tools.util.seven_in_eight import encode as encode_7_8
from midi_tools.message import Message, Parser


@dataclass(frozen=True)
class FileTypeInfoResponseMessage(Message):
    prefix = b"\xF0\x43\x50\x00\x00\x06\x02"

    string: bytes

    def __post_init__(self):
        assert len(self.string) <= 16383

    def to_message(self) -> bytes:
        payload = encode_7_8(self.string)
        length = encode(len(payload))

        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x06,   0x02]) + length + payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "FileTypeInfoResponseMessage":
        parser = Parser(raw)
        parser.expect_literal(cls.prefix)
        length = parser.get_integer(2)
        payload = parser.get_7_in_8(length)
        parser.expect_literal(bytes([0xF7]))
        parser.expect_empty()

        return cls(raw, payload)
