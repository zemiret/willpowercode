from detector import * 
import cv2 as cv

def main():
    cap = cv.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        mask = make_hand_mask(frame)        

        contour = get_hand_contour(mask)
        hull = get_convex_hull(contour)

#        cv.drawContours(frame, hull, -1, (0, 0, 255), 3)

        for i in range(len(hull[0:-1])):
            cv.line(frame, tuple(hull[i][0]), tuple(hull[i + 1][0]), (0, 255, 0), 3)
            cv.circle(frame, tuple(hull[i][0]), 15, (255, 0, 0), 2)

    #    for i in range(defects.shape[0]):
    #        s,e,f,d = defects[i,0]
    #        start = tuple(contour[s][0])
    #        end = tuple(contour[e][0])
    #        far = tuple(contour[f][0])
    #        cv.line(frame, start, end, [0,255,0], 2)
    #        cv.circle(frame, far, 5, [0,0,255], -1)

        # Display the resulting frame
        #cv.drawContours(frame, contour, -1, (0, 255, 0), 3)
        #cv.drawContours(frame, hull, -1, (0, 0, 255), 3)

        cv.imshow('mask', mask)
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

if __name__ == '__main__':
    main()