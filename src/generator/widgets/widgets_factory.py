from generator.execution_observers import NumericKeypadExecutionObserver, PrintObserver
from generator.widgets import GeneratorWidget
from generator.widgets.function import FunctionGeneratorWidget
from generator.widgets.navigation import NavigationGeneratorWidget
from generator.widgets.numeric_keypad import NumericKeypadGeneratorWidget
from generator.widgets.statement import StatementGeneratorWidget
from .top_level import TopLevelGeneratorWidget


class WidgetsFactory(object):
    @staticmethod
    def make_navigation(observer=PrintObserver()) -> GeneratorWidget:
        return NavigationGeneratorWidget(observer)

    @staticmethod
    def make_numeric_keypad(observer=NumericKeypadExecutionObserver()) -> GeneratorWidget:
        return NumericKeypadGeneratorWidget(observer)

    @staticmethod
    def make_statement(observer=PrintObserver()) -> GeneratorWidget:
        return StatementGeneratorWidget(observer)

    @staticmethod
    def make_top_level(observer=PrintObserver()) -> GeneratorWidget:
        return TopLevelGeneratorWidget(observer)

    @staticmethod
    def make_function(observer=PrintObserver()) -> GeneratorWidget:
        return FunctionGeneratorWidget(observer)
