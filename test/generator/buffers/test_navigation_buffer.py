from generator.buffers.navigation_buffer import NavigationBuffer
from generator.exceptions import GeneratorBufferException
from test.common import TestCase


class TestNavigationBuffer(TestCase):
    def setUp(self):
        self.nav_buffer = NavigationBuffer()

    def testInitialState(self):
        self.assertEqual(self.nav_buffer.peek(), (0, 0))

    def test_setting_and_resetting_correct_values(self):
        self.nav_buffer.put((12, 12))
        self.assertEqual(self.nav_buffer.peek(), (12, 12))

        self.nav_buffer.put((100, 120))
        self.assertEqual(self.nav_buffer.peek(), (100, 120))

        self.nav_buffer.clear()
        self.assertEqual(self.nav_buffer.peek(), (0, 0))

    def test_setting_incorrect_values(self):
        self.assertRaises(GeneratorBufferException, lambda: self.nav_buffer.put((-1, 12)))
        self.assertRaises(GeneratorBufferException, lambda: self.nav_buffer.put((0, -12)))
        self.assertRaises(GeneratorBufferException, lambda: self.nav_buffer.put((-100, -100)))
