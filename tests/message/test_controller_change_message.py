import unittest

from midi_tools.message import ControllerChangeMessage


class ControllerChangeMessageTest(unittest.TestCase):
    def test_to_message(self):
        self.assertEqual(b"\xB5\x7B\x0C", ControllerChangeMessage(None, 5, 0x7B, 12).to_message())  # add assertion here

    def test_parse(self):
        raw = b"\xB5\x7B\x0C"
        self.assertEqual(ControllerChangeMessage(raw, 5, 0x7B, 12), ControllerChangeMessage.parse(raw))


if __name__ == '__main__':
    unittest.main()
