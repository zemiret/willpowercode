from queue import Queue, Empty

import cv2 as cv

from detector import Detector


def main():
    cap = cv.VideoCapture(0)
    detector_q_ui_in = Queue()
    detector_q_ui_out = Queue()
    detector_q_input_in = Queue()
    detector_q_input_out = Queue()

    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    roi = ((frame_width // 2, 0), (frame_width - 1, frame_height - 1))

    detector = Detector(detector_q_ui_in,
                        detector_q_ui_out,
                        detector_q_input_in,
                        detector_q_input_out,
                        roi)

    detector.start()

    while True:
        _, frame = cap.read()
        detector_q_ui_in.put(frame)
        res = detector_q_ui_out.get()

        try:
            res_out = detector_q_input_out.get_nowait()
            print(res_out)
        except Empty:
            pass

        cv.imshow('output', res[0])
        cv.imshow('frame', res[1])
        cv.imshow('threshed', res[2])

        key = cv.waitKey(10) & 0xff

        if key == ord('q'):
            detector.stop()
            detector.join()
            cap.release()
            cv.destroyAllWindows()
            break
        else:
            detector_q_input_in.put(key)


if __name__ == "__main__":
    main()
