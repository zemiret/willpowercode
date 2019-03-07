from generator.base import make_generator_entry, make_pop_entry, COMMON_CAPTIONS, make_execute_entry
from generator.execution_observers import ExecutionObserver
from generator.widgets import GeneratorWidget
from test.common import TestCase


class TestConvenienceFunctions(TestCase):
    class DummyWidget(GeneratorWidget):
        def display(self, screen, *args, **kwargs):
            pass

        def handle_input(self, u_in):
            pass

        def reset(self):
            pass

    class DummyObserver(ExecutionObserver):
        def notify(self, u_in: str):
            pass

    def test_make_option_entry(self):
        entry =\
            make_generator_entry(
                'captionStr',
                TestConvenienceFunctions.DummyWidget(TestConvenienceFunctions.DummyObserver())
            )
        self.assertEqual(entry['caption'], 'captionStr')
        self.assertTrue('action' in entry)

    def test_make_pop_entry(self):
        entry = make_pop_entry()
        self.assertEqual(entry['caption'], COMMON_CAPTIONS['back'])
        self.assertTrue('action' in entry)

    def test_make_execute_entry(self):
        entry = make_execute_entry()
        self.assertEqual(entry['caption'], COMMON_CAPTIONS['accept'])
        self.assertTrue('action' in entry)
