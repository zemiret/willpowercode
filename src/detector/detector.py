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
        # self._subtractor = cv.createBackgroundSubtractorMOG2(detectShadows=False, varThreshold=0)
        self._subtractor = cv.bgsegm.createBackgroundSubtractorGSOC(
            mc=cv.bgsegm.LSBP_CAMERA_MOTION_COMPENSATION_LK,
            nSamples=30,
            hitsThreshold=60,
            noiseRemovalThresholdFacBG=0.008,
            noiseRemovalThresholdFacFG=0.016
            # noiseRemovalThresholdFacBG=0.01,
            # noiseRemovalThresholdFacFG=0.01
        )
        self._roi_points = roi

        self._capture_counter = Counter()

        self._stop_evt = Event()
        self._erode_iterations = 1
        self._erode_kernel_size = (3, 3)

        # self._save_next_frame = True
        # self._saved_bg_frame = None

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

            # if self._save_next_frame:
            #     self._saved_bg_frame = cv.blur(roi, (15, 15))
            #     self._save_next_frame = False

            roi = self._prepare_for_extraction(roi)
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

    def _prepare_for_extraction(self, frame):
        # frame = cv.resize(frame, )

        hsv_img = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # multiple by a factor to change the saturation
        hsv_img[..., 1] = hsv_img[..., 1] * 1.4

        # multiple by a factor of less than 1 to reduce the brightness
        hsv_img[..., 2] = hsv_img[..., 2] * 1

        frame = cv.cvtColor(hsv_img, cv.COLOR_HSV2BGR)
        frame = cv.bitwise_not(frame)

        factor = 5
        frame = cv.resize(frame, (frame.shape[1] // factor, frame.shape[0] // factor))
        frame = cv.resize(frame, (frame.shape[1] * factor, frame.shape[0] * factor))

        frame = cv.blur(frame, (5, 5))

        # TOOOOOO SLOW
        # frame = cv.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 21)
        # segments = cv.ximgproc.createSuperpixelSLIC(frame, algorithm=cv.ximgproc.MSLIC, region_size=31)
        # print(segments)

        # vis = np.zeros(frame.shape[:2], dtype="float")

        # loop over each of the unique superpixels
        # for v in np.unique(segments):
            # construct a mask for the segment so we can compute image
            # statistics for *only* the masked region
            # mask = np.ones(frame.shape[:2])
            # mask[segments == v] = 0

            # compute the superpixel colorfulness, then update the
            # visualization array
            # seg_color = self.segment_colorfulness(frame, mask)
            # vis[segments == v] = seg_color

        # frame = vis

        # alpha = 0.2
        # overlay = np.dstack([vis] * 3)
        # output = frame.copy()
        # cv.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame, 8)

        # if self._saved_bg_frame is not None:
        #     frame = frame - self._saved_bg_frame
        # diff = cv.absdiff(frame, self._saved_bg_frame)
        # mask = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)

        # th = 1
        # imask = mask > th
        # canvas = np.zeros_like(self._saved_bg_frame, np.uint8)
        # canvas[imask] = frame[imask]
        #
        # frame = canvas

        return frame

    # def segment_colorfulness(self, image, mask):
    #     # split the image into its respective RGB components, then mask
    #     # each of the individual RGB channels so we can compute
    #     # statistics only for the masked region
    #     (B, G, R) = cv.split(image.astype("float"))
    #     R = np.ma.masked_array(R, mask=mask)
    #     G = np.ma.masked_array(B, mask=mask)
    #     B = np.ma.masked_array(B, mask=mask)
    #
    #     # compute rg = R - G
    #     rg = np.absolute(R - G)
    #
    #     # compute yb = 0.5 * (R + G) - B
    #     yb = np.absolute(0.5 * (R + G) - B)
    #
    #     # compute the mean and standard deviation of both `rg` and `yb`,
    #     # then combine them
    #     stdRoot = np.sqrt((rg.std() ** 2) + (yb.std() ** 2))
    #     meanRoot = np.sqrt((rg.mean() ** 2) + (yb.mean() ** 2))
    #
    #     # derive the "colorfulness" metric and return it
    #     return stdRoot + (0.3 * meanRoot)

    def _get_contours(self, roi):
        fgmask = self._get_fgmask(roi)
        extracted = self._get_foreground(fgmask, roi)
        filtered = self._apply_filters(extracted)

        contours, _ = cv.findContours(filtered, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        return contours, filtered

    def _get_fgmask(self, roi):
        # fgmask = self._subtractor.apply(roi, learningRate=self._bg_subtractor_learning_rate)
        fgmask = self._subtractor.apply(roi, learningRate=0)
        # kernel = np.ones((3, 3), np.uint8)
        fgmask = cv.erode(fgmask, self._erode_kernel_size, iterations=self._erode_iterations)

        return fgmask

    def _get_foreground(self, fgmask, roi):
        extracted = cv.bitwise_and(roi, roi, mask=fgmask)
        extracted = cv.cvtColor(extracted, cv.COLOR_BGR2GRAY)

        return extracted

    def _apply_filters(self, extracted):
        # blurred = cv.blur(extracted, (3, 3))
        # _, thresh = cv.threshold(blurred, 20, 255, cv.THRESH_BINARY)
        _, thresh = cv.threshold(extracted, 30, 255, cv.THRESH_BINARY)
        # thresh = cv.adaptiveThreshold(extracted, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 21, 2)

        thresh = cv.morphologyEx(thresh, cv.MORPH_OPEN, (3, 3), iterations=5)

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

