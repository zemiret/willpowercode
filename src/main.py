import os
from curses import wrapper
from queue import Queue, Empty

import cv2 as cv

from detector import Detector
from generator import GeneratorStateMaster, Commander, WidgetsFactory, GeneratorError


def main(stdscr):
    cap = cv.VideoCapture(0)

    detector, d_ui_in, d_ui_out, d_input_in, d_input_out = setup_detector(cap)
    detector.start()

    gen = setup_generator(stdscr)
    gen.display()

    while True:
        res = read_frame(cap, d_ui_in, d_ui_out)

        try:
            res_out = get_detector_output(d_input_out)

            print(res_out)
            gen.handle_input(res_out)
            gen.display()
        except GeneratorError as e:
            print('Shit happened: {}'.format(e))
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


def setup_detector(cap):
    detector_q_ui_in = Queue()
    detector_q_ui_out = Queue()
    detector_q_input_in = Queue()
    detector_q_input_out = Queue()

    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    roi = ((frame_width // 2, 0), (frame_width - 1, frame_height - 1))
    # roi = ((0, 0), (frame_width // 2, frame_height - 1))

    detector = Detector(detector_q_ui_in,
                        detector_q_ui_out,
                        detector_q_input_in,
                        detector_q_input_out,
                        roi)

    return detector, detector_q_ui_in, detector_q_ui_out, detector_q_input_in, detector_q_input_out


def setup_generator(screen):
    output_file = os.path.join(os.path.realpath(os.environ['HOME']), 'tmp', 'willpower.out')
    commander = Commander()
    commander.init(output_file)

    gen = GeneratorStateMaster()
    gen.init(screen)
    gen.set_start_state(WidgetsFactory.make_top_level())
    gen.reset_state()

    return gen


def display_results(res):
    cv.imshow('output', res[0])
    cv.imshow('frame', res[1])
    cv.imshow('threshed', res[2])


def read_frame(cap, d_ui_in, d_ui_out):
    _, frame = cap.read()
    d_ui_in.put(frame)
    return d_ui_out.get()


def get_detector_output(d_input_out):
    res_out = d_input_out.get_nowait()
    res_out = int(res_out) - 2  # This shall normalize the output to be 0, 1, 2, 3
    return str(res_out)


# --- TESTING BELOW ---
def simulate_keypad_input():
    yield 0
    while True:
        yield 0
        yield 2
        yield 1
        yield 2


def keyboard_main(stdscr):
    gen = setup_generator(stdscr)
    gen.display()

    keymap = {
        '260': '0',  # left
        '259': '1',  # top
        '261': '2',  # right
        '258': '3',  # down
        '48': '0',  # left
        '49': '1',  # top
        '50': '2',  # right
        '51': '3',  # down
    }

    # keypad_gen = simulate_keypad_input()
    while True:
        gen.display()

        # TODO: Test purposes here:
        # ch = next(keypad_gen)
        # gen.handle_input(str(ch))

        ch = stdscr.getch()

        if ch == 113 or ch == 27:
            break

        if str(ch) in keymap:
            gen.handle_input(keymap[str(ch)])


if __name__ == "__main__":
    # TODO: Test with real detector
    # wrapper(main)
    wrapper(keyboard_main)
