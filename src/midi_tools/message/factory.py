from typing import Optional

from midi_tools.message import Message
from midi_tools.message import yamaha


def create_message(data: bytes) -> Optional[Message]:
    if data.startswith(b"\xF0\x43\x50\x00\x00\x00\x01"):
        return yamaha.PingRequestMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x00\x02"):
        return yamaha.PingResponseMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x01\x01"):
        return yamaha.ConnectionRequestMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x01\x02"):
        return yamaha.ConnectionResponseMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x02\x01"):
        return yamaha.InstrumentDataRequestMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x02\x02"):
        return yamaha.InstrumentDataResponseMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x06\x01"):
        return yamaha.FileTypeInfoRequestMessage.parse(data)
    elif data.startswith(b"\xF0\x43\x50\x00\x00\x06\x02"):
        return yamaha.FileTypeInfoResponseMessage.parse(data)
    else:
        return None
