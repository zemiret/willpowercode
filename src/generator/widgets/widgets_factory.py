from generator.execution_observers.observers_factory import ObserversFactory
from generator.widgets import GeneratorWidget


class WidgetsFactory(object):

    @staticmethod
    def make_navigation(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.navigation import NavigationWidget
        return NavigationWidget(observer)

    @staticmethod
    def make_numeric_keypad(observer=ObserversFactory.make_numeric_keypad()) -> GeneratorWidget:
        from generator.widgets.numeric_keypad import NumericKeypadWidget
        return NumericKeypadWidget(observer)

    @staticmethod
    def make_statement(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.statement import StatementWidget
        return StatementWidget(observer)

    @staticmethod
    def make_top_level(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.top_level import TopLevelWidget
        return TopLevelWidget(observer)

    @staticmethod
    def make_function(observer=ObserversFactory.make_function()) -> GeneratorWidget:
        from generator.widgets.function import FunctionWidget
        return FunctionWidget(observer)

    @staticmethod
    def make_write(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.write import WriteWidget
        return WriteWidget(observer)

    @staticmethod
    def make_class(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.classGen import ClassWidget
        return ClassWidget(observer)
