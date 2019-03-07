from generator.buffers.input_buffer import InputBuffer
from test.common import TestCase


class TestInputBuffer(TestCase):
    def setUp(self):
        self.input_buffer = InputBuffer()

    def testInitialState(self):
        self.assertEqual(self.input_buffer.peek(), "")

    def test_setting_and_resetting(self):
        self.input_buffer.put("a")
        self.assertEqual(self.input_buffer.peek(), "a")

        self.input_buffer.put("kanapka")
        self.assertEqual(self.input_buffer.peek(), "akanapka")

        self.input_buffer.put(123)
        self.assertEqual(self.input_buffer.peek(), "akanapka123")

        self.input_buffer.clear()
        self.assertEqual(self.input_buffer.peek(), "")

        self.input_buffer.put("alo")
        self.assertEqual(self.input_buffer.peek(), "alo")
