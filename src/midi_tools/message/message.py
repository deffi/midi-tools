from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Message:
    raw: Optional[bytes]

    def to_message(self) -> bytes:
        raise NotImplementedError

    @classmethod
    def parse(cls, raw: bytes) -> "Message":
        raise NotImplementedError
