from dataclasses import dataclass

from midi_tools.message import Message


@dataclass(frozen=True)
class ControllerChangeMessage(Message):
    prefix = b"0xB0"  # TODO other channels

    channel: int
    controller: int
    value: int

    def __post_init__(self):
        assert 0 <= self.channel < 16
        assert 0 <= self.controller < 128
        assert 0 <= self.value <= 128

    def to_message(self) -> bytes:
        return bytes([0xB0 | self.channel, self.controller, self.value])

    @classmethod
    def parse(cls, raw: bytes) -> "ControllerChangeMessage":
        assert raw[0] & 0xF0 == 0xB0

        channel = raw[0] & 0x0F
        controller = raw[1]
        value = raw[2]

        return cls(raw, channel, controller, value)
