from dataclasses import dataclass
from typing import Optional

from midi_tools.message import factory

@dataclass(frozen=True)
class Message:
    raw: Optional[bytes]

    def __init_subclass__(cls, **kwargs):
        factory.register_class(cls)

    def to_message(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def parse(cls, raw: bytes) -> "Message":
        raise NotImplementedError
