from typing import Sequence, Iterator, TypeVar

S = TypeVar("S", bound=Sequence)


def slices(sequence: S, length: int) -> Iterator[S]:
    for start in range(0, len(sequence), length):
        yield sequence[start:start+length]
