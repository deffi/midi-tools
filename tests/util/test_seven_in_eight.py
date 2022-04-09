import unittest

from midi_tools.util.seven_in_eight import encode_chunk, encode, decode_chunk, decode
from midi_tools.util.hex import parse


class SevenInEightTest(unittest.TestCase):
    def test_encode_chunk(self):
        # All MSBs zero
        self.assertEqual(parse("00 12 23 34 45 56 67 78"), encode_chunk(parse("12 23 34 45 56 67 78")))

        # Some MSBs one
        self.assertEqual(parse("57 12 23 34 45 56 67 78"), encode_chunk(parse("92 23 B4 45 D6 E7 F8")))

        # Shorter chunk
        self.assertEqual(parse("01 32 78"), encode_chunk(parse("32 F8")))
        self.assertEqual(parse("02 32 78"), encode_chunk(parse("B2 78")))
        self.assertEqual(parse("01 78"), encode_chunk(parse("F8")))
        self.assertEqual(parse("00 78"), encode_chunk(parse("78")))

        # Chunk too short or too long
        with self.assertRaises(AssertionError): encode_chunk(parse(""))
        with self.assertRaises(AssertionError): encode_chunk(parse("00 00 00 00 00 00 00 00"))

    def test_encode(self):
        # Empty message
        self.assertEqual(bytes([]), encode(bytes([])))

        # Single chunk (1, 2, and 7 bytes)
        self.assertEqual(parse("00 01"), encode(parse("01")))
        self.assertEqual(parse("00 01 02"), encode(parse("01 02")))
        self.assertEqual(parse("00 01 02 03 04 05 06 07"), encode(parse("01 02 03 04 05 06 07")))

        # Multiple chunks (8 bytes)
        self.assertEqual(parse("00 01 02 03 04 05 06 07 00 08"), encode(parse("01 02 03 04 05 06 07 08")))

    def test_decode_chunk(self):
        # All MSBs zero
        self.assertEqual(parse("12 23 34 45 56 67 78"), decode_chunk(parse("00 12 23 34 45 56 67 78")))

        # Some MSBs one
        self.assertEqual(parse("92 23 B4 45 D6 E7 F8"), decode_chunk(parse("57 12 23 34 45 56 67 78")))

        # Shorter chunk
        self.assertEqual(parse("32 F8"), decode_chunk(parse("01 32 78")))
        self.assertEqual(parse("B2 78"), decode_chunk(parse("02 32 78")))
        self.assertEqual(parse("F8"), decode_chunk(parse("01 78")))
        self.assertEqual(parse("78"), decode_chunk(parse("00 78")))

        # Encoded chunk too short or too long
        with self.assertRaises(AssertionError): decode_chunk(parse(""))
        with self.assertRaises(AssertionError): decode_chunk(parse("00"))
        with self.assertRaises(AssertionError): decode_chunk(parse("00 00 00 00 00 00 00 00 00"))

    def test_decode(self):
        # Empty message
        self.assertEqual(bytes([]), decode(bytes([])))

        # Single chunk (1, 2, and 7 bytes)
        self.assertEqual(parse("01"), decode(parse("00 01")))
        self.assertEqual(parse("01 02"), decode(parse("00 01 02")))
        self.assertEqual(parse("01 02 03 04 05 06 07"), decode(parse("00 01 02 03 04 05 06 07")))

        # Multiple chunks (8 bytes)
        self.assertEqual(parse("01 02 03 04 05 06 07 08"), decode(parse("00 01 02 03 04 05 06 07 00 08")))


if __name__ == '__main__':
    unittest.main()
