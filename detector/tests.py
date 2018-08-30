from detector import *
import cv2 as cv
from algorithms import dbscan


def clusters_check():
    points = [
        (122, 100),
        (125, 105),
        (130, 115),

        (289, 300),
        (250, 310),
        (260, 320),
        (270, 314),
        (280, 300),

        (500, 610),
        (502, 620),
    ]

    print(points)
    clusters, noise = dbscan(points, 15, 1)
    print('\n\n--- result ---')
    print(clusters)
    print(len(clusters))
    print(noise)


def main():
    cap = cv.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        mask = make_hand_mask(frame)

        contour = get_hand_contour(mask)
        hull, defects = get_convex_hull(contour)

        print(hull)
        print(defects)
        print('---')

        points = []

        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(contour[s][0])
            end = tuple(contour[e][0])
            far = tuple(contour[f][0])
            points.append(start)
            cv.line(frame, start, end, [0, 255, 0], 2)
            cv.circle(frame, far, 5, [0, 0, 255], -1)

        clusters, noise = dbscan(points, 45, 1)
        clusters_mid_points = [c[len(c) // 2] for c in clusters]

        for mid_point in clusters_mid_points:
            cv.circle(frame, mid_point, 15, (255, 0, 0), 2)

        #        cv.drawContours(frame, hull, -1, (0, 0, 255), 3)

        # print(hull)

        # for i in range(len(hull[0:-1])):
        # cv.line(frame, tuple(hull[i][0]), tuple(hull[i + 1][0]), (0, 255, 0), 3)
        #     cv.circle(frame, tuple(hull[i][0]), 15, (255, 0, 0), 2)
        #
        # points = [tuple(hull[i][0]) for i in range(len(hull))]

        # print(len(clusters))

        # Display the resulting frame
        # cv.drawContours(frame, contour, -1, (0, 255, 0), 3)
        # cv.drawContours(frame, hull, -1, (0, 0, 255), 3)

        cv.imshow('mask', mask)
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
