import unittest

from midi_tools.util.hex import parse, render


class HexTest(unittest.TestCase):
    def test_render(self):
        self.assertEqual("", render(b""))
        self.assertEqual("FF", render(b"\xFF"))
        self.assertEqual("31 32 33", render(b"123"))

    def test_parse(self):
        self.assertEqual(b"", parse(""))
        self.assertEqual(b"\xFF", parse("FF"))
        self.assertEqual(b"321", parse("33 32 31"))

        with self.assertRaises(AssertionError): parse(" ")
        with self.assertRaises(AssertionError): parse("3")
        with self.assertRaises(AssertionError): parse("345")


if __name__ == '__main__':
    unittest.main()
