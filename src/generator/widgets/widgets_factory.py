from generator.execution_observers.observers_factory import ObserversFactory
from generator.widgets import GeneratorWidget


class WidgetsFactory(object):
    @staticmethod
    def make_navigation(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.navigation import NavigationGeneratorWidget
        return NavigationGeneratorWidget(observer)

    @staticmethod
    def make_numeric_keypad(observer=ObserversFactory.make_numeric_keypad()) -> GeneratorWidget:
        from generator.widgets.numeric_keypad import NumericKeypadGeneratorWidget
        return NumericKeypadGeneratorWidget(observer)

    @staticmethod
    def make_statement(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.statement import StatementGeneratorWidget
        return StatementGeneratorWidget(observer)

    @staticmethod
    def make_top_level(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.top_level import TopLevelGeneratorWidget
        return TopLevelGeneratorWidget(observer)

    @staticmethod
    def make_function(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.function import FunctionGeneratorWidget
        return FunctionGeneratorWidget(observer)
