from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from midi_tools.message import Message

_map = {}


def register_class(cls):
    print(f"Register {cls} as {cls.prefix}")
    _map[cls.prefix] = cls


def create_message(data: bytes) -> Optional[Message]:
    candidates = [cls for prefix, cls in _map.items() if data.startswith(prefix)]

    if len(candidates) == 0:
        return None
    elif len(candidates) == 1:
        return candidates[0].parse(data)
    else:
        raise ValueError(f"Ambiguous message; candidates: {candidates}")
