
from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class FileTypeInfoRequestMessage(Message):
    def to_message(self) -> bytes:
        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x06,   0x01,   0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "FileTypeInfoRequestMessage":
        assert raw == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x06,   0x01,   0xF7])

        return cls(raw)
