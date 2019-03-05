import unittest

from generator import GeneratorStateMaster, WidgetsFactory
from generator.widgets.function import FunctionWidget
from generator.widgets.navigation import NavigationWidget
from generator.widgets.numeric_keypad import NumericKeypadWidget
from generator.widgets.statement import StatementWidget
from generator.widgets.top_level import TopLevelWidget


class TestWidgetsFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GeneratorStateMaster('dumb screen')  # Required setup so that it does not fail resolving

    def test_widgets_creation(self):
        self.assertIsInstance(WidgetsFactory.make_top_level(), TopLevelWidget)
        self.assertIsInstance(WidgetsFactory.make_navigation(), NavigationWidget)
        self.assertIsInstance(WidgetsFactory.make_numeric_keypad(), NumericKeypadWidget)
        self.assertIsInstance(WidgetsFactory.make_statement(), StatementWidget)
        self.assertIsInstance(WidgetsFactory.make_function(), FunctionWidget)


if __name__ == '__main__':
    unittest.main()
