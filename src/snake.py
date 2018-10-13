import curses
from queue import Queue, Empty
from random import randint
import cv2 as cv

from detector import Detector


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


def display_results(res):
    cv.imshow('output', res[0])
    cv.imshow('frame', res[1])
    cv.imshow('threshed', res[2])


def main():
    out = open('/Users/antoni.mleczko/tmp/snake_out', 'a+')

    KEY_RIGHT = 0
    KEY_DOWN = 1
    KEY_LEFT = 2
    KEY_UP = 3

    window_height = 30
    window_width = 100

    curses.initscr()
    win = curses.newwin(window_height, window_width, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)

    key = KEY_RIGHT  # Initializing values
    score = 0

    snake = [[4, 10], [4, 9], [4, 8]]  # Initial snake co-ordinates
    food = [10, 20]  # First food co-ordinates

    win.addch(food[0], food[1], '*')  # Prints the food

    cap = cv.VideoCapture(0)

    detector, d_ui_in, d_ui_out, d_input_in, d_input_out = setup_detector(cap)
    detector.start()

    while True:  # While Esc key is not pressed
        _, frame = cap.read()
        d_ui_in.put(frame)
        res = d_ui_out.get()

        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(score) + ' ')  # Printing 'Score' and
        win.addstr(0, 27, ' SNAKE ')  # 'SNAKE' strings
        # win.timeout(250 - int(len(snake) / 5 + len(snake) / 10) % 120)  # Increases the speed of Snake as its length increases
        win.timeout(120)  # Increases the speed of Snake as its length increases

        prevKey = key  # Previous key pressed

        try:
            key = d_input_out.get_nowait()
            key = int(key) - 2  # This shall normalize the output to be 0, 1, 2, 3
        except (Empty, ValueError):
            pass

        display_results(res)

        if key != prevKey:
            out.write('Key changed %s -> %s\n' % (prevKey, key))
            out.flush()

        if (key - prevKey) % 2 == 0:
            key = prevKey

        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:  # If an invalid key is pressed
            key = prevKey

        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1),
                         snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

        # If snake crosses the boundaries, make it enter from the other side
        if snake[0][0] == 0:
            snake[0][0] = window_height - 2
        if snake[0][1] == 0:
            snake[0][1] = window_width - 2
        if snake[0][0] == window_height - 1:
            snake[0][0] = 1
        if snake[0][1] == window_width - 1:
            snake[0][1] = 1

        # If snake runs over itself
        if snake[0] in snake[1:]:
            out.close()
            detector.stop()
            detector.join()
            cap.release()
            cv.destroyAllWindows()
            # break

        if snake[0] == food:  # When snake eats the food
            food = []
            score += 1
            while not food:
                food = [randint(1, 28), randint(1, 98)]  # Calculating next food's coordinates
                if food in snake:
                    food = []
            win.addch(food[0], food[1], '*')
        else:
            last = snake.pop()  # [1] If it does not eat the food, length decreases
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '#')

        win.refresh()

        keyboard_key = cv.waitKey(10) & 0xff
        if keyboard_key == ord('q'):
            detector.stop()
            detector.join()
            cap.release()
            cv.destroyAllWindows()
            break
        else:
            d_input_in.put(keyboard_key)

    curses.endwin()
    print("\nScore - " + str(score))


if __name__ == "__main__":
    main()
