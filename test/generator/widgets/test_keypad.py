from generator.exceptions import GeneratorError
from generator.execution_observers.observers_factory import ObserversFactory
from generator.widgets.keypad import KeypadWidget
from test.common import TestCase


class TestKeypadWidget(TestCase):
    def setUp(self):
        self.keypad_widget = KeypadWidget(ObserversFactory.make_stub())

    def test_random_handle_input_out_of_range(self):
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('0000'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('0001'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('400'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('500'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('401'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('abc'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('333'))
        self.assertRaises(GeneratorError, lambda: self.keypad_widget.handle_input('322'))

    def test_adding_letters(self):
        self.keypad_widget._internal_buffer = 'abc'

        self.keypad_widget.handle_input('000')
        self.assertEqual(self.keypad_widget._internal_buffer, 'abca')

        self.keypad_widget.handle_input('223')
        self.assertEqual(self.keypad_widget._internal_buffer, 'abcaz')

        self.keypad_widget.handle_input('112')
        self.assertEqual(self.keypad_widget._internal_buffer, 'abcazl')

    def test_deleting_letters(self):
        self.keypad_widget._internal_buffer = 'abc'

        self.keypad_widget.handle_input('301')
        self.assertEqual(self.keypad_widget._internal_buffer, 'ab')

        self.keypad_widget.handle_input('301')
        self.assertEqual(self.keypad_widget._internal_buffer, 'a')

        self.keypad_widget.handle_input('301')
        self.assertEqual(self.keypad_widget._internal_buffer, '')

        self.keypad_widget.handle_input('301')
        self.assertEqual(self.keypad_widget._internal_buffer, '')
