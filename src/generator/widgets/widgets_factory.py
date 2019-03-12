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
        from generator.widgets.class_gen import ClassWidget
        return ClassWidget(observer)

    @staticmethod
    def make_refactor(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.refactor import RefactorWidget
        return RefactorWidget(observer)

    @staticmethod
    def make_common(observer=ObserversFactory.make_stub()) -> GeneratorWidget:
        from generator.widgets.common_gen import CommonWidget
        return CommonWidget(observer)

    @staticmethod
    def make_keypad(observer=ObserversFactory.make_keypad()) -> GeneratorWidget:
        from generator.widgets.keypad import KeypadWidget
        return KeypadWidget(observer)
