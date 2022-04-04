#!/usr/bin/env python

from typing import List

import typer

app = typer.Typer()


@app.command()
def encode(value: str):
    value = int(value, 0)
    result = []

    while value > 0:
        result.insert(0, value % 128)
        value = value // 128

    print(" ".join(f"{x:02x}" for x in result))

@app.command()
def decode(values: List[str]):
    result = 0
    for value in values:
        part = int(value, 16)
        assert 0 <= part < 128

        result = result * 128 + part

    print(f"0x{result:X} = {result}")

def calculate_checksum(values: List[str]):
    sum = 0
    for value in values:
        part = int(value, 16)
        assert 0 <= part < 128
        sum += part

    sum = sum % 128

    return 128 - sum

@app.command()
def checksum(values: List[str]):
    checksum = calculate_checksum(values)
    print(f"0x{checksum:02x}")

@app.command()
def verify(values: List[str]):
    expected = calculate_checksum(values[:-1])
    actual = int(values[-1], 16)

    if expected == actual:
        print("OK")
    else:
        print(f"Expected checksum: {expected:02x}, actual: {actual:02x}")



if __name__ == "__main__":
    app()
