import cv2 as cv
import numpy as np 


def make_hand_mask(img):
    skin_lower = lambda hue: np.array([hue, 0.05 * 255, 0.05 * 255])
    skin_upper = lambda hue: np.array([hue, 0.9 * 255, 0.8 * 255])

    img_hls = cv.cvtColor(img, cv.COLOR_BGR2HLS)
    range_mask = cv.inRange(img_hls, skin_lower(0), skin_upper(20))


    blurred = cv.blur(range_mask, (10, 10))
    _, threshed = cv.threshold(blurred, 200, 255, cv.THRESH_BINARY)

    return threshed

def get_hand_contour(mask):
    # get all contours and return the biggest one
    _, contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    return max(contours, key=lambda ct: cv.contourArea(ct))


def get_convex_hull(contour):
    hull = cv.convexHull(contour)
    # defects = cv.convexityDefects(contour, hull)
    return hull