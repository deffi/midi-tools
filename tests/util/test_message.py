import unittest

from midi_tools.util.hex import parse as h
from midi_tools.util.message import encode, decode, checksum, checksum_valid


class MessageTest(unittest.TestCase):
    def test_encode(self):
        # Default length
        self.assertEqual(b"", encode(0))
        self.assertEqual(h("01"), encode(1))
        self.assertEqual(h("7F"), encode(0x7F))
        self.assertEqual(h("01 00"), encode(0x80))
        self.assertEqual(h("7F 7F"), encode(0x3FFF))
        self.assertEqual(h("01 00 00"), encode(0x4000))

        # Minimum length
        self.assertEqual(h("00"), encode(0, minimum_length=1))
        self.assertEqual(h("00 00"), encode(0, minimum_length=2))

        self.assertEqual(h("7F"), encode(0x7F, minimum_length=1))
        self.assertEqual(h("00 7F"), encode(0x7F, minimum_length=2))
        self.assertEqual(h("00 00 7F"), encode(0x7F, minimum_length=3))

        # Exact length
        with self.assertRaises(ValueError): encode(0x3FFF, length=1)
        self.assertEqual(h("7F 7F"), encode(0x3FFF, length=2))
        self.assertEqual(h("00 7F 7F"), encode(0x3FFF, length=3))

        # Invalid parameters
        with self.assertRaises(AssertionError): encode(0x01, length=2, minimum_length=3)

    def test_decode(self):
        self.assertEqual(0, decode(b""))
        self.assertEqual(1, decode(h("01")))
        self.assertEqual(0x7F, decode(h("7F")))
        self.assertEqual(0x80, decode(h("01 00")))
        self.assertEqual(0x3FFF, decode(h("7F 7F")))
        self.assertEqual(0x4000, decode(h("01 00 00")))

    def test_checksum(self):
        # Empty message
        self.assertEqual(h("00"), checksum(h("")))

        # Single byte
        self.assertEqual(h("00"), checksum(h("00")))
        self.assertEqual(h("7F"), checksum(h("01")))
        self.assertEqual(h("7E"), checksum(h("02")))
        self.assertEqual(h("01"), checksum(h("7F")))

        # Multiple bytes
        self.assertEqual(h("00"), checksum(h("00 00 00")))
        self.assertEqual(h("7A"), checksum(h("01 02 03")))
        self.assertEqual(h("7E"), checksum(h("02 01 7F")))
        self.assertEqual(h("06"), checksum(h("7D 7E 7F")))

        # Value out of range
        with self.assertRaises(ValueError): checksum(h("80"))

    def test_checksum_valid(self):
        # Empty
        with self.assertRaises(ValueError):
            checksum_valid(h(""))

        # Good
        self.assertTrue(checksum_valid(h("00")))
        self.assertTrue(checksum_valid(h("01 02 03 7A")))

        # Bad
        self.assertFalse(checksum_valid(h("01")))
        self.assertFalse(checksum_valid(h("01 02 03 A5")))


if __name__ == '__main__':
    unittest.main()
