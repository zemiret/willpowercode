import glob

import numpy as np
import os
from curses import wrapper
from queue import Queue, Empty

import cv2 as cv

from detector import Detector
from generator import GeneratorStateMaster, Commander
from generator.buffers import GeneratorBuffers
from generator.exceptions import GeneratorError
from generator.widgets import WidgetsFactory


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

    buffers = GeneratorBuffers()

    gen = GeneratorStateMaster()
    gen.init(screen, buffers)
    gen.set_start_state(WidgetsFactory.make_top_level())
    gen.reset_state()

    return gen


def display_results(res):
    cv.imshow('output', res[0])
    # cv.imshow('frame', res[1])
    cv.imshow('threshed', res[2])
    cv.imshow('roi', res[3])


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


def detector_main():
    cap = cv.VideoCapture(0)

    detector, d_ui_in, d_ui_out, d_input_in, d_input_out = setup_detector(cap)
    detector.start()

    while True:
        res = read_frame(cap, d_ui_in, d_ui_out)

        try:
            res_out = get_detector_output(d_input_out)
            print(res_out)
        except (Empty, ValueError):
            pass

        display_results(res)

        key = cv.waitKey(5) & 0xff
        if key == ord('q'):
            detector.stop()
            detector.join()
            cap.release()
            cv.destroyAllWindows()
            break
        else:
            d_input_in.put(key)


def setup_test_detector(cap, subtractor):
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
                        roi,
                        subtractor)

    return detector, detector_q_ui_in, detector_q_ui_out, detector_q_input_in, detector_q_input_out


def test_main():
    cap = cv.VideoCapture('/Users/antoni.mleczko/dev/willpowercode/resources/testMovie.mov')

    detectors = {
        'KNN': cv.createBackgroundSubtractorKNN(detectShadows=False),
        'MOG': cv.bgsegm.createBackgroundSubtractorMOG(),
        'MOG2': cv.createBackgroundSubtractorMOG2(detectShadows=False),
        'GMG': cv.bgsegm.createBackgroundSubtractorGMG(),
        'CNT': cv.bgsegm.createBackgroundSubtractorCNT(),
        'GSOC': cv.bgsegm.createBackgroundSubtractorGSOC(),
        'LSBP': cv.bgsegm.createBackgroundSubtractorLSBP(),
    }

    det_setups = []

    for name, detector in detectors.items():
        detector_with_name = (name, setup_test_detector(cap, detector))
        det_setups.append(detector_with_name)
        detector_with_name[1][0].start()

    # skip 130 frames:
    for i in range(130):
        cap.read()

    # send reset to all detectors:
    for dset in det_setups:
        dset[1][3].put('c')

    while cap.isOpened():
        print('Ya in loop?')

        ret, frame = cap.read()
        step_res = []

        if ret is True:
            for dset in det_setups:
                dset[1][1].put(frame)
                res = dset[1][2].get(block=True)
                cv.putText(res[0], dset[0], (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2, cv.LINE_AA)
                step_res.append(res)

            horizontal1 = np.hstack([step_res[i][0] for i in range(4)])
            horizontal2 = np.hstack([step_res[i][0] for i in range(4, 7)] + [step_res[0][0]])

            stack = np.vstack([horizontal1, horizontal2])

            cv.imshow('res', stack)
        else:
            break

        key = cv.waitKey(1) & 0xff
        if key == ord('q'):
            # generate_video(results)
            for dset in det_setups:
                dset[1][0].stop()
                dset[1][0].join()
                cap.release()
                cv.destroyAllWindows()
            break

    # generate_video(results)

    for dset in det_setups:
        dset[1][0].stop()
        dset[1][0].join()
        cap.release()
        cv.destroyAllWindows()


# def generate_video(img):
#     folder = '/Users/antoni.mleczko/dev/willpowercode/resources'
#
#     # for i in range(len(img)):
#     print(img[1][0])
#     # cv.imshow('whatever', img[1][0][1])
#     plt.imshow(img[1][0][1])
#     plt.yticks([])
#     plt.xticks([])
#     cv.waitKey(0)
#     plt.show()
#     # plot_subplots(img[1])
#     # plt.show()
#         # plt.savefig(folder + "/file%02d.png" % i)
#
#     # os.chdir(folder)
#     # os.subprocess.call([
#     #     'ffmpeg', '-framerate', '8', '-i', 'file%02d.png', '-r', '30', '-pix_fmt', 'yuv420p',
#     #     'video_name.mp4'
#     # ])
#     # for file_name in glob.glob("*.png"):
#         # os.remove(file_name)
#         # print(file_name)


def plot_subplots(results):
    for index, (name, frame) in enumerate(results):
        plot_img(index, name, frame)


def plot_img(index, title, img):
    plt.subplot(2, 4, index)
    plt.imshow(img)
    plt.title(title)
    plt.xticks([])
    plt.yticks([])


if __name__ == "__main__":
    # wrapper(main)
    # wrapper(keyboard_main)
    # detector_main()
    test_main()
