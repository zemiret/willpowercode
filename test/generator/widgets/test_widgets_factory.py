import unittest

from generator.widgets import WidgetsFactory
from generator.widgets.common_gen import CommonWidget
from generator.widgets.function import FunctionWidget
from generator.widgets.keypad import KeypadWidget
from generator.widgets.navigation import NavigationWidget
from generator.widgets.numeric_keypad import NumericKeypadWidget
from generator.widgets.refactor import RefactorWidget
from generator.widgets.statement import StatementWidget
from generator.widgets.top_level import TopLevelWidget
from test.common import TestCase


class TestWidgetsFactory(TestCase):
    def test_widgets_creation(self):
        self.assertIsInstance(WidgetsFactory.make_top_level(), TopLevelWidget)
        self.assertIsInstance(WidgetsFactory.make_navigation(), NavigationWidget)
        self.assertIsInstance(WidgetsFactory.make_numeric_keypad(), NumericKeypadWidget)
        self.assertIsInstance(WidgetsFactory.make_statement(), StatementWidget)
        self.assertIsInstance(WidgetsFactory.make_function(), FunctionWidget)
        self.assertIsInstance(WidgetsFactory.make_refactor(), RefactorWidget)
        self.assertIsInstance(WidgetsFactory.make_common(), CommonWidget)
        self.assertIsInstance(WidgetsFactory.make_keypad(), KeypadWidget)


if __name__ == '__main__':
    unittest.main()
