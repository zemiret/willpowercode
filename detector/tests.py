import math
import cv2 as cv
import numpy as np

from detector import Detector


def main():
    cap = cv.VideoCapture(0)
    learning_rate = 0
    subtractor = cv.createBackgroundSubtractorMOG2()


    while True:
        _, frame = cap.read()
        frame = cv.bilateralFilter(frame, 5, 50, 100)

        frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        roi_p1 = (frame_width // 2, 0)
        roi_p2 = (frame_width - 1, frame_height - 1)
        cv.rectangle(frame, roi_p1, roi_p2, (0, 0, 255), 2)
        roi = frame[roi_p1[1]:roi_p2[1], roi_p1[0]:roi_p2[0]]

        fgmask = subtractor.apply(roi, learningRate=learning_rate)
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
                    prev_far = None

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
                            cv.circle(drawing, start, 8, (0, 255, 0), 2)
                            cv.circle(drawing, far, 8, [211, 84, 0], -1)
                            cv.circle(drawing, end, 8, (0, 0, 255), 2)

                            if prev_far is not None:
                                cv.circle(drawing, prev_far, 15, (0, 0, 255), -1)

                        prev_far = far

                        print(cnt + 1)

        cv.imshow('output', drawing)
        cv.imshow('capture', frame)
        # cv.imshow('extracted', extracted)
        # cv.imshow('blurred', blurred)
        cv.imshow('threshed', thresh)

        key = cv.waitKey(10) & 0xff
        if key == ord('q'):
            break
        elif key == ord('c'):
            subtractor = cv.createBackgroundSubtractorMOG2()

    cap.release()
    cv.destroyAllWindows()


def detector_test():
    det = Detector()

    while True:
        print(det.count())

if __name__ == '__main__':
    # main()
    detector_test()
