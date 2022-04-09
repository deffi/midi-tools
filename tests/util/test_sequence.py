import unittest

from midi_tools.util.sequence import slices


class TestSequence(unittest.TestCase):
    def test_slice(self):
        self.assertEqual([], list(slices("", 3)))
        self.assertEqual(["abc", "def"], list(slices("abcdef", 3)))
        self.assertEqual(["abc", "def", "g"], list(slices("abcdefg", 3)))

        self.assertEqual([b"abc", b"def", b"g"], list(slices(b"abcdefg", 3)))


if __name__ == '__main__':
    unittest.main()
