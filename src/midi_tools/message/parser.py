from midi_tools.util import message, seven_in_eight

class ParseError(ValueError):
    ...

class Parser:
    def __init__(self, raw: bytes):
        self._raw = raw
        self._data = raw

    @property
    def raw(self) -> bytes:
        return self._raw

    @property
    def data(self) -> bytes:
        return self._data

    def expect_literal(self, expected: bytes):
        if not self._data.startswith(expected):
            raise ParseError(f"Data does not start with {expected}")

        self._data = self._data[len(expected):]

        return expected

    def expect_empty(self):
        if len(self._data) > 0:
            raise ParseError(f"Data is not empty")

    def get_data(self, length: int) -> bytes:
        if len(self._data) < length:
            raise ParseError(f"Data does not have {length} bytes remaining")

        result = self._data[0:length]
        self._data = self._data[length:]

        return result

    def get_integer(self, length: int) -> int:
        return message.decode(self.get_data(length))

    def get_7_in_8(self, length):
        return seven_in_eight.decode(self.get_data(length))
