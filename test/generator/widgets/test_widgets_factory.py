import unittest

from generator import GeneratorStateMaster, WidgetsFactory
from generator.widgets.function import FunctionGeneratorWidget
from generator.widgets.navigation import NavigationGeneratorWidget
from generator.widgets.numeric_keypad import NumericKeypadGeneratorWidget
from generator.widgets.statement import StatementGeneratorWidget
from generator.widgets.top_level import TopLevelGeneratorWidget


class TestWidgetsFactory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GeneratorStateMaster('dumb screen')  # Required setup so that it does not fail resolving

    def test_widgets_creation(self):
        self.assertIsInstance(WidgetsFactory.make_top_level(), TopLevelGeneratorWidget)
        self.assertIsInstance(WidgetsFactory.make_navigation(), NavigationGeneratorWidget)
        self.assertIsInstance(WidgetsFactory.make_numeric_keypad(), NumericKeypadGeneratorWidget)
        self.assertIsInstance(WidgetsFactory.make_statement(), StatementGeneratorWidget)
        self.assertIsInstance(WidgetsFactory.make_function(), FunctionGeneratorWidget)


if __name__ == '__main__':
    unittest.main()
