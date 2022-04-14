from dataclasses import dataclass

from midi_tools.util.message import encode
from midi_tools.util.seven_in_eight import encode as encode_7_8
from midi_tools.message import Message


@dataclass(frozen=True)
class FileTypeInfoResponseMessage(Message):
    string: bytes

    def __post_init__(self):
        assert len(self.string) <= 16383

    def to_message(self) -> bytes:
        payload = encode_7_8(self.string)
        length = encode(len(payload))

        return bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x06,   0x02]) + length + payload + bytes([0xF7])

    @classmethod
    def parse(cls, raw: bytes) -> "FileTypeInfoResponseMessage":
        raise NotImplementedError
        # # f0 43 50   0 0 2   len data
        # assert len(raw) >= 7
        # assert raw[0:7] == bytes([0xF0, 0x43, 0x50,   0x00, 0x00, 0x02,   0x02])
        # length = raw[7]
        # assert len(raw) == 7 + length + 1
        # payload = raw[7:7+length]
        # assert raw[7+length] == bytes([0xF7])
        #
        # return cls(raw, payload)
