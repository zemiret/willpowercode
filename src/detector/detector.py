import math
from queue import Empty, Full
from collections import Counter
from threading import Thread, Event

import cv2 as cv
import numpy as np


class Detector(Thread):
    """
        Class used for deciding recognized fingers count.
        Since it is a subclass of thread, read these few lines and constructor parameters to get it working properly.

        When you are detecting, make sure that the background is not changing (lightning conditions as well).
        The detector works for counting fingers, there is one quirk though - it does not detect the empty hand and treats
        it as one.
    """
    def __init__(self, q_ui_in, q_ui_out, q_input_in, q_input_out, roi, **kwargs):
        """
        Args:
            q_ui_in (Queue): Queue for pushing registered frame
            q_ui_out (Queue): Queue that the results will be pushed to as a triplet (output, threshed, input)
            q_input_in (Queue): Queue that the input can be pushed into
            q_input_out (Queue): Queue that the output from the detector will be put into (the most important one!)
            roi (tuple): A tuple of points that span the rectangular ROI (region of interest)
        """
        super(Detector, self).__init__(**kwargs)

        self._q_ui_in = q_ui_in
        self._q_ui_out = q_ui_out
        self._q_input_in = q_input_in
        self._q_input_out = q_input_out

        self._bg_subtractor_learning_rate = 0
        self._subtractor = cv.createBackgroundSubtractorMOG2(detectShadows=False, varThreshold=0)
        self._roi_points = roi

        self._capture_counter = Counter()

        self._stop_evt = Event()
        self._erode_iterations = 1

    def run(self):
        while True:
            if self.stopped():
                print('Stopping detector')
                return

            self._handle_key_input()

            try:
                frame = self._q_ui_in.get_nowait()   # not blocking get, for otherwise the thread cannot be joined
            except Empty:
                continue

            self._draw_roi(frame)
            roi = self._get_roi(frame)
            contours, threshed = self._get_contours(roi)
            canvas = np.zeros(roi.shape, np.uint8)

            fingers_count = None
            if len(contours) > 0:
                fingers_count = self._detect_fingers_count(contours, canvas)

            self._update_fingers_counter(fingers_count)
            self._push_frames(canvas, frame, threshed, roi)

    def _reset_subtractor(self):
        self._subtractor = cv.createBackgroundSubtractorMOG2(varThreshold=0)

    def _handle_key_input(self):
        try:
            user_input = self._q_input_in.get_nowait()
            self._handle_input(user_input)
        except Empty:
            pass

    def _handle_input(self, user_input):
        if user_input == ord('c'):
            self._reset_subtractor()
        elif user_input == ord('m'):
            self._erode_iterations += 1
        elif user_input == ord('l'):
            if self._erode_iterations > 0:
                self._erode_iterations -= 1

    def _draw_roi(self, frame):
        cv.rectangle(frame, self._roi_points[0], self._roi_points[1], (0, 0, 255), 2)

    def _get_roi(self, frame):
        frame = cv.bilateralFilter(frame, 5, 50, 100)

        roi_p1 = self._roi_points[0]
        roi_p2 = self._roi_points[1]
        roi = frame[roi_p1[1]:roi_p2[1], roi_p1[0]:roi_p2[0]]

        return roi

    def _get_contours(self, roi):
        fgmask = self._get_fgmask(roi)
        extracted = self._get_foreground(fgmask, roi)
        filtered = self._apply_filters(extracted)

        _, contours, _ = cv.findContours(filtered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours, filtered

    def _get_fgmask(self, roi):
        fgmask = self._subtractor.apply(roi, learningRate=self._bg_subtractor_learning_rate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv.erode(fgmask, kernel, iterations=self._erode_iterations)

        return fgmask

    def _get_foreground(self, fgmask, roi):
        extracted = cv.bitwise_and(roi, roi, mask=fgmask)
        extracted = cv.cvtColor(extracted, cv.COLOR_BGR2GRAY)

        return extracted

    def _apply_filters(self, extracted):
        blurred = cv.blur(extracted, (10, 10))
        _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)

        return thresh

    def _draw_contours(self, canvas, max_contour, hull_drawing):
        cv.drawContours(canvas, [max_contour], 0, (0, 255, 0), 2)
        cv.drawContours(canvas, [hull_drawing], 0, (255, 0, 0), 2)

    def _calculate_fingers_count(self, defects, max_contour):
        fingers_count = 0
        defect_points = []

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
                fingers_count += 1

                defect_points.append(far)
        fingers_count += 1

        return fingers_count, defect_points

    def _mark_defect_points(self, defect_points, canvas):
        for defect_point in defect_points:
            cv.circle(canvas, defect_point, 8, [211, 84, 0], -1)

    def _detect_fingers_count(self, contours, canvas):
        max_contour = max(contours, key=lambda c: cv.contourArea(c))
        hull_drawing = cv.convexHull(max_contour)
        self._draw_contours(canvas, max_contour, hull_drawing)

        hull = cv.convexHull(max_contour, returnPoints=False)
        fingers_count = None

        if len(hull) > 3:
            defects = cv.convexityDefects(max_contour, hull)

            if defects is not None:
                fingers_count, defect_points = self._calculate_fingers_count(defects, max_contour)
                self._mark_defect_points(defect_points, canvas)

        return fingers_count

    def _update_fingers_counter(self, fingers_count):
        if fingers_count is None or fingers_count == 1:
            most_common = self._capture_counter.most_common(1)
            if most_common:
                self._q_input_out.put(most_common[0][0])    # most_common is a list of tuples
                self._capture_counter = Counter()   # renew reference
        else:
            self._capture_counter[fingers_count] += 1

    def _push_frames(self, canvas, frame, threshed, roi):
        try:
            self._q_ui_out.put_nowait((canvas, frame, threshed, roi))
        except Full:
            pass

    def stop(self):
        self._stop_evt.set()

    def stopped(self):
        return self._stop_evt.is_set()

