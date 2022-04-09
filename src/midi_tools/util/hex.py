def render(data: bytes) -> str:
    def render_single(value: int) -> str:
        assert 0 <= value < 256
        return f"{value:02X}"

    return " ".join(render_single(d) for d in data)


def parse(string: str) -> bytes:
    def parse_single(value: str) -> int:
        assert len(value) == 2
        return int(value, 16)

    if len(string) == 0:
        return b""
    else:
        parts = string.split(" ")
        return bytes(parse_single(p) for p in parts)
