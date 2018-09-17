import math
from queue import Full
from threading import Thread

import cv2 as cv
import numpy as np


"""
    Class used for deciding recognized fingers count.
    Since it is a subclass of thread, read these few lines and constructor parameters to get it working properly.
    Quick guide:
    * Create a Detector object with proper parameters
    * Call .start() on the object
    * When you want to start intercepting results (that is finger count from the detector), set start_capture_event
      and from this point you can read from the q_out that you passed to the constructor
    * When you want to stop intercepting results, set stop_capture_event
    
    When you are detecting, make sure that the background is not changing (lightning conditions as well).
    If the background got messed up, click 'c' to clear and reset the background subtractor.
    The detector works for counting fingers, there is one quirk though - it does not detect the empty hand and treats
    it as one.
    
"""
class Detector(Thread):
    """
    :param Queue q_out: queue that will be used to put captured results into
    :param Event start_capture_event: event used to notify detector that it can start detecting (and writing a result)
    :param Event stop_capture_event: event used to notify detector that it can stop detecting (and clear a queue)
    """
    def __init__(self, q_out, start_capture_evt, stop_capture_evt):
        super(Detector, self).__init__()

        self._q_out = q_out
        self._start_capture_evt = start_capture_evt
        self._stop_capture_evt = stop_capture_evt
        self.is_capturing = False

        self._cap = cv.VideoCapture(0)
        self._bg_subtractor_learning_rate = 0
        self._subtractor = cv.createBackgroundSubtractorMOG2()
        frame_width = int(self._cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self._cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self._roi_points = ((0, 0), (frame_width // 2, frame_height - 1))

    def run(self):
        while True:
            if self._start_capture_evt.is_set():
                self._start_capturing()
            if self._stop_capture_evt.is_set():
                self._stop_capturing()

            _, frame = self._cap.read()
            frame = cv.bilateralFilter(frame, 5, 50, 100)

            roi_p1 = self._roi_points[0]
            roi_p2 = self._roi_points[1]
            cv.rectangle(frame, roi_p1, roi_p2, (0, 0, 255), 2)
            roi = frame[roi_p1[1]:roi_p2[1], roi_p1[0]:roi_p2[0]]

            fgmask = self._subtractor.apply(roi, learningRate=self._bg_subtractor_learning_rate)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv.erode(fgmask, kernel, iterations=2)
            extracted = cv.bitwise_and(roi, roi, mask=fgmask)
            extracted = cv.cvtColor(extracted, cv.COLOR_BGR2GRAY)

            blurred = cv.blur(extracted, (10, 10))
            _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)

            _, contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            drawing = np.zeros(roi.shape, np.uint8)

            count = None

            if len(contours) > 0:
                max_contour = max(contours, key=lambda c: cv.contourArea(c))
                hull_drawing = cv.convexHull(max_contour)
                cv.drawContours(drawing, [max_contour], 0, (0, 255, 0), 2)
                cv.drawContours(drawing, [hull_drawing], 0, (255, 0, 0), 2)

                hull = cv.convexHull(max_contour, returnPoints=False)
                if len(hull) > 3:
                    defects = cv.convexityDefects(max_contour, hull)

                    if defects is not None:
                        count = 0
                        for i in range(defects.shape[0]):  # calculate the angle
                            s, e, f, d = defects[i][0]
                            start = tuple(max_contour[s][0])
                            end = tuple(max_contour[e][0])
                            far = tuple(max_contour[f][0])

                            a = (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
                            b = (far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2
                            c = (end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2
                            angle = math.acos((b + c - a) / (2 * math.sqrt(b * c)))  # cosine theorem
                            if angle <= math.pi / 2:  # angle less than 90 degree, treat as fingers
                                count += 1
                                cv.circle(drawing, far, 8, [211, 84, 0], -1)
                        count += 1

            cv.imshow('output', drawing)
            cv.imshow('capture', frame)
            cv.imshow('threshed', thresh)

            key = cv.waitKey(20) & 0xff
            if key == ord('c'):
                self._reset_subtractor()

            self._add_result(count)

            if count is None or count == 1:
                self._stop_capture_evt.set()
            else:
                self._start_capture_evt.set()


    def join(self, timeout=None):
        self._cap.release()
        cv.destroyAllWindows()
        super(Detector, self).join(timeout)

    def _stop_capturing(self):
        self.is_capturing = False
        self._stop_capture_evt.clear()
        with self._q_out.mutex:
            self._q_out.queue.clear()

    def _start_capturing(self):
        self.is_capturing = True
        self._start_capture_evt.clear()

    def _reset_subtractor(self):
        self._subtractor = cv.createBackgroundSubtractorMOG2(varThreshold=0)

    def _add_result(self, count):
        if self.is_capturing is False:
            return

        # Try to put an item in the queue, if it's full empty it
        try:
            self._q_out.put(count, timeout=0.1)
        except Full:
            with self._q_out.mutex:
                self._q_out.queue.clear()
