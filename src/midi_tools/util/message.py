def encode(value: int, minimum_length: int = None, length: int = None) -> bytes:
    assert not (minimum_length is not None and length is not None)

    result = []

    while value > 0:
        result.insert(0, value % 128)
        value = value // 128

    if minimum_length is not None:
        pad_length = minimum_length
    elif length is not None:
        if len(result) > length:
            raise ValueError(f"Value {value} does not fit in {length} bytes")

        pad_length = length
    else:
        pad_length = None

    if pad_length is not None and len(result) < pad_length:
        result = [0] * (pad_length - len(result)) + result

    return bytes(result)


def decode(data: bytes) -> int:
    result = 0
    for value in data:
        if not 0 <= value < 128:
            raise ValueError(f"Value out of range: {value}")

        result = result * 128 + value

    return result


def checksum(values: bytes) -> bytes:
    total = 0
    for value in values:
        if not 0 <= value < 128:
            raise ValueError(f"Value out of range: {value}")

        total += value

    # 0 ->  0
    # 1 -> 7F
    # 2 -> 7E
    # ...
    # 7F -> 1
    result = 127 - ((total-1) % 128)

    return bytes([result])


def checksum_valid(values: bytes) -> bool:
    if len(values) == 0:
        raise ValueError(f"No checksum present")

    expected = checksum(values[:-1])
    actual = values[-1:]

    return actual == expected
