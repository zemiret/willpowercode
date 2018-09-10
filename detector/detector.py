import math
from collections import Counter

import cv2 as cv
import numpy as np

"""
    Class used for deciding recognized fingers count
"""
class Detector(object):
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.bg_subtractor_learning_rate = 0
        self.subtractor = cv.createBackgroundSubtractorMOG2()
        frame_width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.roi_points = ((frame_width // 2, 0), (frame_width - 1, frame_height - 1))

    def __del__(self):
        self.cap.release()
        cv.destroyAllWindows()

    def count(self):
        return Counter(self._stream_results(200)).most_common(1)[0]

    def _read_count(self):
        _, frame = self.cap.read()
        frame = cv.bilateralFilter(frame, 5, 50, 100)

        roi_p1 = self.roi_points[0]
        roi_p2 = self.roi_points[1]
        cv.rectangle(frame, roi_p1, roi_p2, (0, 0, 255), 2)
        roi = frame[roi_p1[1]:roi_p2[1], roi_p1[0]:roi_p2[0]]

        fgmask = self.subtractor.apply(roi, learningRate=self.bg_subtractor_learning_rate)
        kernel = np.ones((3, 3), np.uint8)
        fgmask = cv.erode(fgmask, kernel, iterations=1)
        extracted = cv.bitwise_and(roi, roi, mask=fgmask)
        extracted = cv.cvtColor(extracted, cv.COLOR_BGR2GRAY)

        blurred = cv.blur(extracted, (15, 15))
        _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)

        _, contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        drawing = np.zeros(roi.shape, np.uint8)

        if len(contours) > 0:
            max_contour = max(contours, key=lambda c: cv.contourArea(c))
            hull_drawing = cv.convexHull(max_contour)
            cv.drawContours(drawing, [max_contour], 0, (0, 255, 0), 2)
            cv.drawContours(drawing, [hull_drawing], 0, (255, 0, 0), 2)

            hull = cv.convexHull(max_contour, returnPoints=False)
            if len(hull) > 3:
                defects = cv.convexityDefects(max_contour, hull)

                if defects is not None:
                    cnt = 0
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
                            cnt += 1
                            cv.circle(drawing, far, 8, [211, 84, 0], -1)

                        yield cnt + 1
        else:
            yield None

        cv.imshow('output', drawing)
        cv.imshow('capture', frame)
        cv.imshow('threshed', thresh)

        key = cv.waitKey(10) & 0xff
        if key == ord('c'):
            self.subtractor = cv.createBackgroundSubtractorMOG2(varThreshold=0)

    def _stream_results(self, times=None):
        counter = self._read_count()
        if times:
            for i in range(times):
                yield next(counter)
        else:
            while True:
                yield next(counter)
