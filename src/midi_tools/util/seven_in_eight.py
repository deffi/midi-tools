from midi_tools.util.sequence import slices


def encode_chunk(data: bytes) -> bytes:
    assert 1 <= len(data) <= 7

    msbs = int("".join("1" if d >= 0x80 else "0" for d in data), 2)
    lsbs = (b & 0x7F for b in data)

    return bytes([msbs]) + bytes(lsbs)


def encode(raw: bytes) -> bytes:
    encoded_chunks = (encode_chunk(chunk) for chunk in slices(raw, 7))
    return b"".join(encoded_chunks)


def decode_chunk(data: bytes) -> bytes:
    assert 2 <= len(data) <= 8

    lsbs = data[1:]
    msbs = f"{data[0]:0{len(lsbs)}b}"

    if len(msbs) != len(lsbs):
        raise ValueError("Extra MSBs in chunk: {data}")

    return bytes(lsb + 0x80 * int(msb) for msb, lsb in zip(msbs, lsbs))


def decode(encoded: bytes) -> bytes:
    decoded_chunks = (decode_chunk(chunk) for chunk in slices(encoded, 8))
    return b"".join(decoded_chunks)
