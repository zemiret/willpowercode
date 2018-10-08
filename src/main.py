import os
from curses import wrapper
from queue import Queue, Empty

import cv2 as cv

from detector import Detector
from generator import GeneratorMaster, TopLevelGenerator


def setup_detector(cap):
    detector_q_ui_in = Queue()
    detector_q_ui_out = Queue()
    detector_q_input_in = Queue()
    detector_q_input_out = Queue()

    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # roi = ((frame_width // 2, 0), (frame_width - 1, frame_height - 1))
    roi = ((0, 0), (frame_width // 2, frame_height - 1))

    detector = Detector(detector_q_ui_in,
                        detector_q_ui_out,
                        detector_q_input_in,
                        detector_q_input_out,
                        roi)

    return detector, detector_q_ui_in, detector_q_ui_out, detector_q_input_in, detector_q_input_out


def setup_generator():
    output_file = os.path.join(os.path.realpath(os.environ['HOME']), 'tmp', 'willpower.out')
    gen = GeneratorMaster(output_file)
    gen.set_start_state(TopLevelGenerator())
    gen.reset_state()
    return gen


def display_results(res):
    cv.imshow('output', res[0])
    cv.imshow('frame', res[1])
    cv.imshow('threshed', res[2])


def main(stdscr):
    cap = cv.VideoCapture(0)

    detector, d_ui_in, d_ui_out, d_input_in, d_input_out = setup_detector(cap)
    detector.start()

    gen = setup_generator()
    gen.display(stdscr)

    while True:
        _, frame = cap.read()
        d_ui_in.put(frame)
        res = d_ui_out.get()

        try:
            res_out = d_input_out.get_nowait()
            res_out = int(res_out) - 2      # This shall normalize the output to be 0, 1, 2, 3

            gen.handle_input(res_out)
            gen.display(stdscr)
        except (Empty, ValueError):
            pass

        display_results(res)

        key = cv.waitKey(10) & 0xff
        if key == ord('q'):
            detector.stop()
            detector.join()
            cap.release()
            cv.destroyAllWindows()
            break
        else:
            d_input_in.put(key)


if __name__ == "__main__":
    wrapper(main)


