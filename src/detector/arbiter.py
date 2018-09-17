from collections import Counter
from queue import Queue, Empty
from threading import Thread, Event

from detector import Detector


class Arbiter(Thread):
    def __init__(self):
        super(Arbiter, self).__init__()

        self.input_detected_evt = Event()
        self.q_out = Queue()

        self._start_capture_evt = Event()
        self._stop_capture_evt = Event()
        self._q_capture = Queue()
        self._detector = None

        self._capture_counter = Counter()

    def start(self):
        super(Arbiter, self).start()
        self._detector = Detector(self._q_capture, self._start_capture_evt, self._stop_capture_evt)
        self._detector.start()

    def run(self):
        while True:
            self._start_capture_evt.wait()
            while self._detector.is_capturing:
                try:
                    ct = self._q_capture.get(timeout=0.1)
                    self._capture_counter[ct] += 1
                except Empty:
                    pass
            most_common = self._capture_counter.most_common(1)
            if most_common != []:
                self._detected_result(most_common[0][0])    # most_common is a list of tuples

    def _detected_result(self, res):
        self.q_out.put(res)
        self.input_detected_evt.set()
        self._capture_counter = Counter()
