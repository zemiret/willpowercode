from generator.widgets.function import FunctionGeneratorWidget
from generator.widgets.navigation import NavigationGeneratorWidget
from generator.widgets.numeric_keypad import NumericKeypadGeneratorWidget
from generator.widgets.statement import StatementGeneratorWidget
from .top_level import TopLevelGeneratorWidget


class WidgetsFactory(object):
    @staticmethod
    def make_navigation():
        return NavigationGeneratorWidget()

    @staticmethod
    def make_numeric_keypad():
        return NumericKeypadGeneratorWidget()

    @staticmethod
    def make_statement():
        return StatementGeneratorWidget()

    @staticmethod
    def make_top_level():
        return TopLevelGeneratorWidget()

    @staticmethod
    def make_function():
        return FunctionGeneratorWidget()
